import streamlit as st
import sqlite3
from database import get_db_connection
from gemini_service import get_menu_recommendations
from datetime import datetime

def render_customer_view():
    st.markdown("<h2 class='glow-text-cyan'>📱 Scan-to-Order Digital Menu</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#a0aec0;'>Experience real-time item availability and smart pairing recommendations.</p>", unsafe_allow_html=True)

    # Initialize cart in session state
    if "cart" not in st.session_state:
        st.session_state.cart = {} # {item_id: quantity}
        
    # Table selection binding simulation
    if "table_number" not in st.session_state:
        st.session_state.table_number = "Table 1"
        
    col_t1, col_t2 = st.columns([1, 3])
    with col_t1:
        st.session_state.table_number = st.selectbox(
            "Bound Table:",
            ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5"]
        )
    with col_t2:
        st.info(f"Connected to table terminal binding: **{st.session_state.table_number}**")
        
    # Fetch menu items
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, category, is_available, stock_level FROM menu_items")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Categorize items
    categories = {}
    for item in items:
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
        
    # Display menu
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
                
                # Layout for menu item card
                st.markdown(f"---")
                col_info, col_act = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"**{name}** — **${price:.2f}**")
                    st.markdown(f"<small style='color:#a0aec0;'>{desc}</small>", unsafe_allow_html=True)
                    
                    # Live Availability Badge
                    if not available:
                        st.markdown("<span class='badge badge-critical'>Sold Out</span>", unsafe_allow_html=True)
                    elif stock <= 5:
                        st.markdown(f"<span class='badge badge-medium'>Only {stock} Left</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='badge badge-low'>Available ({stock} in stock)</span>", unsafe_allow_html=True)
                        
                with col_act:
                    if available:
                        if st.button(f"Add to Order", key=f"add_{item_id}"):
                            if item_id in st.session_state.cart:
                                if st.session_state.cart[item_id] < stock:
                                    st.session_state.cart[item_id] += 1
                                    st.success(f"Added another {name}!")
                                else:
                                    st.warning("Cannot add more. Stock limit reached.")
                            else:
                                st.session_state.cart[item_id] = 1
                                st.success(f"Added {name}!")
                    else:
                        st.button("Add to Order", key=f"add_{item_id}", disabled=True)

    # Sidebar Cart & Checkout Summary
    st.sidebar.markdown("<h3 class='glow-text-purple'>🛒 Your Order Cart</h3>", unsafe_allow_html=True)
    if not st.session_state.cart:
        st.sidebar.write("Cart is empty. Tap items to add them.")
    else:
        cart_total = 0.0
        items_in_cart_objects = []
        
        # Display items in cart
        for item_id, qty in list(st.session_state.cart.items()):
            # Find item details
            item = next((i for i in items if i['id'] == item_id), None)
            if item:
                name = item['name']
                price = item['price']
                sub = price * qty
                cart_total += sub
                items_in_cart_objects.append({"id": item_id, "name": name, "price": price, "qty": qty})
                
                st.sidebar.markdown(f"**{name}** x{qty} — **${sub:.2f}**")
                
                col_cart_sub, col_cart_add, col_cart_del = st.sidebar.columns(3)
                with col_cart_sub:
                    if st.button("➖", key=f"sub_c_{item_id}", width="stretch"):
                        st.session_state.cart[item_id] -= 1
                        if st.session_state.cart[item_id] <= 0:
                            del st.session_state.cart[item_id]
                        st.rerun()
                with col_cart_add:
                    if st.button("➕", key=f"add_c_{item_id}", width="stretch"):
                        if qty < item['stock_level']:
                            st.session_state.cart[item_id] += 1
                            st.rerun()
                        else:
                            st.sidebar.error("Stock limit reached!")
                with col_cart_del:
                    if st.button("❌", key=f"del_c_{item_id}", width="stretch"):
                        del st.session_state.cart[item_id]
                        st.rerun()
                        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"#### Subtotal: **${cart_total:.2f}**")
        
        # Gemini AI Personalized Pairing Recommendation
        st.sidebar.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        st.sidebar.markdown("<h4 class='glow-text-cyan'>✨ Gemini Pairing Suggestion</h4>", unsafe_allow_html=True)
        
        rec = get_menu_recommendations(items_in_cart_objects)
        suggested_name = rec.get("suggested_item_name", "Truffle Fries")
        reason = rec.get("recommendation_reason", "A perfect side to complement your selections!")
        
        # Find suggested item ID and price
        suggested_item = next((i for i in items if i['name'] == suggested_name), None)
        
        if suggested_item and suggested_item['id'] not in st.session_state.cart:
            st.sidebar.markdown(f"**Try {suggested_name}** (${suggested_item['price']:.2f})")
            st.sidebar.markdown(f"<p style='font-size:0.85rem; color:#00f2fe; line-height:1.2;'>\"{reason}\"</p>", unsafe_allow_html=True)
            if st.sidebar.button(f"Add Suggestion", key="add_ai_rec"):
                st.session_state.cart[suggested_item['id']] = 1
                st.success(f"Added {suggested_name} to cart!")
                st.rerun()
        else:
            st.sidebar.write("Your cart has the ultimate pairing match!")
            
        st.sidebar.markdown("---")
        
        # Checkout button
        if st.sidebar.button("🚀 Place Table Order", type="primary", width="stretch"):
            # Write order to database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            now_str = datetime.now().isoformat()
            
            # Insert orders record
            cursor.execute(
                "INSERT INTO orders (table_number, status, subtotal, discount, total, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (st.session_state.table_number, 'pending', cart_total, 0.0, cart_total, now_str)
            )
            order_id = cursor.lastrowid
            
            # Insert order items and deduct inventory/menu stocks
            for item_id, qty in st.session_state.cart.items():
                item = next((i for i in items if i['id'] == item_id), None)
                unit_price = item['price'] if item else 0.0
                
                cursor.execute(
                    "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order_id, item_id, qty, unit_price)
                )
                
                # Deduct stock level
                cursor.execute(
                    "UPDATE menu_items SET stock_level = max(0, stock_level - ?) WHERE id = ?",
                    (qty, item_id)
                )
                
            conn.commit()
            conn.close()
            
            # Reset cart
            st.session_state.cart = {}
            st.sidebar.success(f"Order #{order_id} placed successfully! The kitchen has received your order.")
            st.toast("Kitchen preparing your meal!", icon="🔥")
            st.rerun()
            
    # Active orders for this table summary
    st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
    st.markdown("### 🕒 Active Table Orders Status")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, status, total, created_at FROM orders WHERE table_number = ? AND status != 'completed' AND status != 'voided' ORDER BY id DESC",
        (st.session_state.table_number,)
    )
    active_orders = cursor.fetchall()
    conn.close()
    
    if not active_orders:
        st.write("No active orders for this table at the moment.")
    else:
        for order in active_orders:
            o_id = order['id']
            status = order['status']
            total = order['total']
            
            # Show status with coloring
            if status == 'pending':
                status_html = "<span class='badge badge-medium'>Sent to Kitchen</span>"
            elif status == 'preparing':
                status_html = "<span class='badge badge-low'>Preparing / Cooking</span>"
            else:
                status_html = f"<span class='badge'>{status}</span>"
                
            st.markdown(f"**Order #{o_id}** — Total: ${total:.2f} — State: {status_html}", unsafe_allow_html=True)
