import streamlit as st
import sqlite3
from database import get_db_connection
from gemini_service import get_menu_recommendations
from datetime import datetime

def render_customer_view(user):
    st.markdown("<h2 class='glow-indigo'>📱 Scan-to-Order Digital Menu</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Real-time availability, smart pairings, and seamless checkout.</p>", unsafe_allow_html=True)

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    if "table_number" not in st.session_state:
        st.session_state.table_number = "Table 1"

    col_t1, col_t2 = st.columns([1, 3])
    with col_t1:
        st.session_state.table_number = st.selectbox(
            "📍 Bound Table:",
            ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5"]
        )
    with col_t2:
        st.info(f"Connected to: **{st.session_state.table_number}**")

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

                st.markdown(f"---")
                col_info, col_qty, col_act = st.columns([4, 1, 1])

                with col_info:
                    st.markdown(f"**{name}** — **${price:.2f}**")
                    st.markdown(f"<small style='color:#94a3b8;'>{desc}</small>", unsafe_allow_html=True)
                    if not available:
                        st.markdown("<span class='badge badge-critical'>Sold Out</span>", unsafe_allow_html=True)
                    elif stock <= 5:
                        st.markdown(f"<span class='badge badge-medium'>Only {stock} Left</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='badge badge-low'>In Stock ({stock})</span>", unsafe_allow_html=True)

                with col_qty:
                    if available:
                        st.number_input("Qty", min_value=1, max_value=stock, value=1,
                                        key=f"qty_{item_id}", label_visibility="collapsed")
                    else:
                        st.number_input("Qty", min_value=0, max_value=0, value=0,
                                        key=f"qty_{item_id}", disabled=True, label_visibility="collapsed")

                with col_act:
                    if available:
                        if st.button(f"Add", key=f"add_{item_id}", use_container_width=True):
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
                    else:
                        st.button("Add", key=f"add_{item_id}", disabled=True, use_container_width=True)

    # --- Sidebar Cart ---
    st.sidebar.markdown("<h3 class='glow-pink'>🛒 Your Order</h3>", unsafe_allow_html=True)
    if not st.session_state.cart:
        st.sidebar.markdown("<p style='color:#94a3b8;'>Cart is empty. Add items from the menu!</p>", unsafe_allow_html=True)
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

                st.sidebar.markdown(f"**{name}** x{qty} — **${sub:.2f}**")
                c1, c2, c3 = st.sidebar.columns(3)
                with c1:
                    if st.button("➖", key=f"sub_{item_id}", use_container_width=True):
                        st.session_state.cart[item_id] -= 1
                        if st.session_state.cart[item_id] <= 0:
                            del st.session_state.cart[item_id]
                        st.rerun()
                with c2:
                    if st.button("➕", key=f"plu_{item_id}", use_container_width=True):
                        if qty < item['stock_level']:
                            st.session_state.cart[item_id] += 1
                            st.rerun()
                with c3:
                    if st.button("❌", key=f"del_{item_id}", use_container_width=True):
                        del st.session_state.cart[item_id]
                        st.rerun()

        st.sidebar.markdown("---")

        # AI Recommendation
        st.sidebar.markdown("<h4 class='glow-indigo'>✨ Smart Pairing</h4>", unsafe_allow_html=True)
        rec = get_menu_recommendations(items_in_cart_objects)
        suggested_name = rec.get("suggested_item_name", "Truffle Fries")
        reason = rec.get("recommendation_reason", "A perfect complement!")
        suggested_item = next((i for i in items if i['name'] == suggested_name), None)
        if suggested_item and suggested_item['id'] not in st.session_state.cart:
            st.sidebar.markdown(f"**Try {suggested_name}** (${suggested_item['price']:.2f})")
            st.sidebar.markdown(f"<p style='font-size:0.82rem; color:#6366f1;'>\"{reason}\"</p>", unsafe_allow_html=True)
            if st.sidebar.button("Add Suggestion", key="add_rec", use_container_width=True):
                st.session_state.cart[suggested_item['id']] = 1
                st.rerun()

        st.sidebar.markdown("---")

        # Clear Cart
        if st.sidebar.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

        # Tax, Tip, Payment
        tax_rate = 0.0875
        tax = round(cart_total * tax_rate, 2)
        st.sidebar.markdown(f"Subtotal: **${cart_total:.2f}**")
        st.sidebar.markdown(f"Tax (8.75%): **${tax:.2f}**")

        tip_pct = st.sidebar.slider("💬 Tip %", 0, 30, 20, key="tip_slider")
        tip = round(cart_total * tip_pct / 100, 2)
        st.sidebar.markdown(f"Tip ({tip_pct}%): **${tip:.2f}**")

        grand_total = cart_total + tax + tip
        st.sidebar.markdown(f"""
        <div class="tip-highlight">
            <div style="font-size:0.8rem; color:#92400e; font-weight:600;">TOTAL</div>
            <div style="font-size:1.6rem; font-weight:800; color:#92400e;">${grand_total:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        payment_method = st.sidebar.radio(
            "💳 Payment:", ["Cash", "Card", "Mobile Pay"],
            horizontal=True, key="pay_method"
        )

        if tip_pct > 0:
            st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(6,182,212,0.08));
                 border-radius: 12px; padding: 10px; margin: 8px 0; border: 1px solid rgba(16,185,129,0.2);
                 text-align:center;">
                <span style="font-size:0.85rem; color:#059669; font-weight:600;">
                    💚 Your waiter will earn ${tip:.2f} tip!
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.sidebar.markdown("---")

        if st.sidebar.button("🚀 Place Order", type="primary", use_container_width=True):
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

            # Receipt
            receipt = f"""<div style="background: linear-gradient(135deg, #ecfdf5, #f0fdf4); border: 2px solid #10b981;
                 border-radius: 16px; padding: 20px; margin: 10px 0;">
                <h3 style="color:#059669; margin:0; text-align:center;">✅ Order Placed!</h3>
                <div style="text-align:center; margin:8px 0;">
                    <span class="badge badge-low">Order #{order_id}</span>
                </div>
                <div style="font-size:0.85rem; color:#1e293b; line-height:1.8; margin-top:10px;">"""
            for item_id, qty in st.session_state.cart.items():
                item = next((i for i in items if i['id'] == item_id), None)
                if item:
                    receipt += f"{item['name']} x{qty} — ${item['price']*qty:.2f}<br>"
            receipt += f"""---
                Subtotal: ${cart_total:.2f}<br>
                Tax: ${tax:.2f}<br>
                Tip: ${tip:.2f}<br>
                <b>Total: ${grand_total:.2f}</b><br>
                Payment: {payment_method}
                </div></div>"""
            st.sidebar.markdown(receipt, unsafe_allow_html=True)

            st.session_state.cart = {}
            st.toast("Kitchen is on it!", icon="🔥")
            st.rerun()

    # Active orders
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🕒 Active Orders")
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
        st.markdown("<p style='color:#94a3b8;'>No active orders for this table.</p>", unsafe_allow_html=True)
    else:
        for order in active_orders:
            o_id = order['id']
            status = order['status']
            total = order['total']
            if status == 'pending':
                badge = "<span class='badge badge-medium'>Sent to Kitchen</span>"
            elif status == 'preparing':
                badge = "<span class='badge badge-indigo'>Preparing</span>"
            else:
                badge = f"<span class='badge badge-low'>{status}</span>"
            st.markdown(f"""
            <div class="glass-card" style="padding:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong>Order #{o_id}</strong>
                    <span style="font-weight:700; color:#6366f1;">${total:.2f}</span>
                </div>
                <div style="margin-top:6px;">{badge}</div>
            </div>
            """, unsafe_allow_html=True)
