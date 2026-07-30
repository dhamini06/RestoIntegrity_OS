import streamlit as st
import sqlite3
from database import get_db_connection, add_notification
from gemini_service import get_menu_recommendations
from datetime import datetime

def render_customer_view(user):
    st.markdown("<h2 style='font-weight:700; color:#FAFAFA; font-size:1.4rem; margin-bottom:4px;'>Scan-to-Order Digital Menu</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#71717A; font-size:0.85rem; margin-bottom:20px;'>Real-time availability, smart pairings, and seamless checkout.</p>", unsafe_allow_html=True)

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    if "table_number" not in st.session_state:
        st.session_state.table_number = "Table 1"

    col_t1, col_t2 = st.columns([1, 3])
    with col_t1:
        st.session_state.table_number = st.selectbox(
            "Table",
            ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5"]
        )
    with col_t2:
        st.markdown(f"""
        <div class='glass-card-subtle' style='padding:8px 16px; display:inline-block;'>
            <span style='color:#71717A; font-size:0.82rem;'>Connected to: </span>
            <span style='color:#C9A86A; font-weight:600; font-size:0.85rem;'>{st.session_state.table_number}</span>
        </div>
        """, unsafe_allow_html=True)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, category, is_available, stock_level FROM menu_items")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()

    categories = {}
    for item in items:
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    tabs = st.tabs(list(categories.keys()))
    for tab, cat_name in zip(tabs, categories.keys()):
        with tab:
            for item in categories[cat_name]:
                item_id = item['id']
                name = item['name']
                desc = item['description']
                price = item['price']
                stock = item['stock_level']
                available = item['is_available'] == 1 and stock > 0

                st.markdown(f"""
                <div class="glass-card" style="padding:16px; display:flex; justify-content:space-between; align-items:center;">
                    <div style="flex:1;">
                        <div style="display:flex; align-items:center; gap:8px;">
                            <strong style="color:#FAFAFA; font-size:0.95rem;">{name}</strong>
                            <span style="color:#C9A86A; font-weight:700; font-size:0.95rem;">${price:.2f}</span>
                        </div>
                        <p style="color:#71717A; font-size:0.8rem; margin:4px 0 0;">{desc}</p>
                        <div style="margin-top:6px;">""", unsafe_allow_html=True)
                if not available:
                    st.markdown("<span class='badge badge-critical'>Sold Out</span>", unsafe_allow_html=True)
                elif stock <= 5:
                    st.markdown(f"<span class='badge badge-medium'>Only {stock} Left</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='badge badge-low'>In Stock ({stock})</span>", unsafe_allow_html=True)
                st.markdown("</div></div>", unsafe_allow_html=True)

                if available:
                    c_qty, c_add = st.columns([1, 1])
                    with c_qty:
                        st.number_input("Qty", min_value=1, max_value=stock, value=1,
                                        key=f"qty_{item_id}", label_visibility="collapsed")
                    with c_add:
                        if st.button("Add", key=f"add_{item_id}", use_container_width=True):
                            qty_val = st.session_state.get(f"qty_{item_id}", 1)
                            if item_id in st.session_state.cart:
                                new_qty = st.session_state.cart[item_id] + qty_val
                                if new_qty <= stock:
                                    st.session_state.cart[item_id] = new_qty
                                else:
                                    st.warning("Stock limit!")
                            else:
                                st.session_state.cart[item_id] = qty_val
                            st.rerun()

    st.sidebar.markdown(f"""
    <div style="background: #1F1F23; border-radius: 16px; padding: 16px; margin: 0 0 16px 0;
        border: 1px solid rgba(255,255,255,0.06);">
        <div style="font-size:0.85rem; font-weight:600; color:#FAFAFA; letter-spacing:0.01em;">
            Your Order
        </div>
        <div style="font-size:0.75rem; color:#71717A; margin-top:2px;">{st.session_state.table_number}</div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.cart:
        st.sidebar.markdown("<p style='color:#71717A; font-size:0.82rem; text-align:center; padding:20px 0;'>Cart is empty. Add items from the menu.</p>", unsafe_allow_html=True)
    else:
        cart_total = 0.0
        items_in_cart_objects = []

        for item_id, qty in list(st.session_state.cart.items()):
            item = next((i for i in items if i['id'] == item_id), None)
            if item:
                name = item['name']
                price = item['price']
                sub = price * qty
                cart_total += sub
                items_in_cart_objects.append({"id": item_id, "name": name, "price": price, "qty": qty})

                st.sidebar.markdown(f"""
                <div style="background:#18181B; border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:10px; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="color:#FAFAFA; font-size:0.85rem; font-weight:500;">{name}</span>
                        <span style="color:#C9A86A; font-weight:600; font-size:0.85rem;">${sub:.2f}</span>
                    </div>
                    <div style="display:flex; gap:4px; margin-top:6px;">
                """, unsafe_allow_html=True)
                c1, c2, c3 = st.sidebar.columns(3)
                with c1:
                    if st.button("-", key=f"sub_{item_id}", use_container_width=True):
                        st.session_state.cart[item_id] -= 1
                        if st.session_state.cart[item_id] <= 0:
                            del st.session_state.cart[item_id]
                        st.rerun()
                with c2:
                    if st.button("+", key=f"plu_{item_id}", use_container_width=True):
                        if qty < item['stock_level']:
                            st.session_state.cart[item_id] += 1
                            st.rerun()
                with c3:
                    if st.button("x", key=f"del_{item_id}", use_container_width=True):
                        del st.session_state.cart[item_id]
                        st.rerun()

        st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        rec = get_menu_recommendations(items_in_cart_objects)
        suggested_name = rec.get("suggested_item_name", "Truffle Fries")
        reason = rec.get("recommendation_reason", "A perfect complement!")
        suggested_item = next((i for i in items if i['name'] == suggested_name), None)
        if suggested_item and suggested_item['id'] not in st.session_state.cart:
            st.sidebar.markdown(f"""
            <div style="background:rgba(201,168,106,0.04); border:1px solid rgba(201,168,106,0.1); border-radius:12px; padding:12px; margin-bottom:12px;">
                <div style="font-size:0.75rem; color:#C9A86A; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; margin-bottom:4px;">Smart Pairing</div>
                <div style="font-size:0.85rem; color:#FAFAFA; font-weight:500;">{suggested_name} <span style="color:#C9A86A;">(${suggested_item['price']:.2f})</span></div>
                <p style="font-size:0.78rem; color:#71717A; margin:4px 0 8px;">"{reason}"</p>
            """, unsafe_allow_html=True)
            if st.sidebar.button("Add Suggestion", key="add_rec", use_container_width=True):
                st.session_state.cart[suggested_item['id']] = 1
                st.rerun()
            st.sidebar.markdown("</div>", unsafe_allow_html=True)

        st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        if st.sidebar.button("Clear Cart", key="clear_cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

        tax_rate = 0.0875
        tax = round(cart_total * tax_rate, 2)
        st.sidebar.markdown(f"""
        <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#71717A; margin:4px 0;">
            <span>Subtotal</span><span style="color:#A1A1AA;">${cart_total:.2f}</span>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#71717A; margin:4px 0;">
            <span>Tax (8.75%)</span><span style="color:#A1A1AA;">${tax:.2f}</span>
        </div>
        """, unsafe_allow_html=True)

        tip_pct = st.sidebar.slider("Tip %", 0, 30, 20, key="tip_slider")
        tip = round(cart_total * tip_pct / 100, 2)
        st.sidebar.markdown(f"""
        <div style="display:flex; justify-content:space-between; font-size:0.82rem; color:#71717A; margin:4px 0;">
            <span>Tip ({tip_pct}%)</span><span style="color:#A1A1AA;">${tip:.2f}</span>
        </div>
        """, unsafe_allow_html=True)

        grand_total = cart_total + tax + tip
        st.sidebar.markdown(f"""
        <div style="background:#1F1F23; border:1px solid rgba(201,168,106,0.1); border-radius:14px; padding:14px; margin:12px 0; text-align:center;">
            <div style="font-size:0.72rem; color:#71717A; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">Total</div>
            <div style="font-size:1.6rem; font-weight:700; color:#C9A86A;">${grand_total:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        payment_method = st.sidebar.radio(
            "Payment", ["Cash", "Card", "Mobile Pay"],
            horizontal=True, key="pay_method"
        )

        if tip_pct > 0:
            st.sidebar.markdown(f"""
            <div style="background:rgba(34,197,94,0.04); border:1px solid rgba(34,197,94,0.1); border-radius:12px; padding:10px; text-align:center;">
                <span style="font-size:0.78rem; color:#22C55E; font-weight:500;">Waiter earns ${tip:.2f} tip</span>
            </div>
            """, unsafe_allow_html=True)

        st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        if st.sidebar.button("Place Order", type="primary", use_container_width=True):
            conn = get_db_connection()
            cursor = conn.cursor()
            now_str = datetime.now().isoformat()

            cursor.execute("""
                INSERT INTO orders (table_number, status, subtotal, discount, total, tax, tip,
                    payment_method, served_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (st.session_state.table_number, 'pending', cart_total, 0.0, grand_total,
                  tax, tip, payment_method, user['username'], now_str))
            order_id = cursor.lastrowid

            for item_id, qty in st.session_state.cart.items():
                item = next((i for i in items if i['id'] == item_id), None)
                unit_price = item['price'] if item else 0.0
                cursor.execute(
                    "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order_id, item_id, qty, unit_price)
                )
                cursor.execute(
                    "UPDATE menu_items SET stock_level = max(0, stock_level - ?) WHERE id = ?",
                    (qty, item_id)
                )
            conn.commit()
            conn.close()

            receipt_items = ""
            for item_id, qty in st.session_state.cart.items():
                item = next((i for i in items if i['id'] == item_id), None)
                if item:
                    receipt_items += f"<div style='display:flex; justify-content:space-between; font-size:0.82rem; color:#A1A1AA;'><span>{item['name']} x{qty}</span><span>${item['price']*qty:.2f}</span></div>"

            st.sidebar.markdown(f"""
            <div style="background:#1F1F23; border:1px solid rgba(34,197,94,0.15); border-radius:16px; padding:20px; margin:10px 0;">
                <div style="text-align:center; margin-bottom:12px;">
                    <div style="width:36px; height:36px; border-radius:50%; background:rgba(34,197,94,0.1);
                        display:flex; align-items:center; justify-content:center; margin:0 auto 8px;
                        border:1px solid rgba(34,197,94,0.1);">
                        <span style="color:#22C55E; font-weight:600; font-size:0.9rem;">&#10003;</span>
                    </div>
                    <div style="color:#22C55E; font-weight:600; font-size:0.9rem;">Order Placed</div>
                    <span class="badge badge-low" style="margin-top:4px;">Order #{order_id}</span>
                </div>
                <div style="margin-top:10px;">
                    {receipt_items}
                    <div class='divider'></div>
                    <div style='display:flex; justify-content:space-between; font-size:0.82rem; color:#71717A;'><span>Subtotal</span><span style='color:#A1A1AA;'>${cart_total:.2f}</span></div>
                    <div style='display:flex; justify-content:space-between; font-size:0.82rem; color:#71717A;'><span>Tax</span><span style='color:#A1A1AA;'>${tax:.2f}</span></div>
                    <div style='display:flex; justify-content:space-between; font-size:0.82rem; color:#71717A;'><span>Tip</span><span style='color:#A1A1AA;'>${tip:.2f}</span></div>
                    <div style='display:flex; justify-content:space-between; font-size:0.95rem; color:#C9A86A; font-weight:700; margin-top:6px;'><span>Total</span><span>${grand_total:.2f}</span></div>
                    <div style='font-size:0.75rem; color:#71717A; margin-top:4px;'>{payment_method}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            add_notification(
                f"New Order #{order_id}",
                f"Order #{order_id} placed at {st.session_state.table_number}. Total: ${grand_total:.2f}. Payment: {payment_method}.",
                role="admin"
            )
            st.session_state.cart = {}
            st.toast("Kitchen is on it!", icon=None)
            st.rerun()

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin-bottom:12px;'>Active Orders</h3>", unsafe_allow_html=True)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, status, total, created_at FROM orders
        WHERE table_number = ? AND status NOT IN ('completed', 'voided')
        ORDER BY id DESC
    """, (st.session_state.table_number,))
    active_orders = cursor.fetchall()
    conn.close()

    if not active_orders:
        st.markdown("<p style='color:#71717A; font-size:0.85rem;'>No active orders for this table.</p>", unsafe_allow_html=True)
    else:
        for order in active_orders:
            o_id = order['id']
            status = order['status']
            total = order['total']
            if status == 'pending':
                badge = "<span class='badge badge-medium'>Sent to Kitchen</span>"
            elif status == 'preparing':
                badge = "<span class='badge badge-blue'>Preparing</span>"
            else:
                badge = f"<span class='badge badge-low'>{status}</span>"
            st.markdown(f"""
            <div class="glass-card" style="padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#FAFAFA; font-size:0.85rem;">Order #{o_id}</strong>
                    <span style="font-weight:600; color:#C9A86A;">${total:.2f}</span>
                </div>
                <div style="margin-top:6px;">{badge}</div>
            </div>
            """, unsafe_allow_html=True)
