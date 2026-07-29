import streamlit as st
import sqlite3
from database import get_db_connection
from integrity_engine import check_void_anomaly
from datetime import datetime

def restore_stock(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT menu_item_id, quantity FROM order_items WHERE order_id = ?", (order_id,))
    items = cursor.fetchall()
    for item in items:
        cursor.execute(
            "UPDATE menu_items SET stock_level = stock_level + ? WHERE id = ?",
            (item['quantity'], item['menu_item_id'])
        )
    conn.commit()
    conn.close()

def update_order_status(order_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    if status == 'preparing':
        cursor.execute("UPDATE orders SET status = ?, prepping_at = ? WHERE id = ?", (status, now_str, order_id))
    elif status == 'completed':
        cursor.execute("UPDATE orders SET status = ?, completed_at = ? WHERE id = ?", (status, now_str, order_id))
    else:
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()

def render_kitchen_view(user):
    st.markdown("<h2 style='font-weight:700; color:#FAFAFA; font-size:1.4rem; margin-bottom:4px;'>Kitchen Order Dispatcher</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#71717A; font-size:0.85rem; margin-bottom:20px;'>Manage live tickets, track cook times, and coordinate service.</p>", unsafe_allow_html=True)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.table_number, o.status, o.subtotal, o.created_at, o.served_by
        FROM orders o
        WHERE o.status IN ('pending', 'preparing')
        ORDER BY o.id ASC
    """)
    active_orders = [dict(row) for row in cursor.fetchall()]

    order_items = {}
    if active_orders:
        order_ids = [o['id'] for o in active_orders]
        placeholders = ','.join('?' * len(order_ids))
        cursor.execute(f"""
            SELECT oi.order_id, oi.quantity, mi.name
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id IN ({placeholders})
        """, order_ids)
        for item in cursor.fetchall():
            o_id = item['order_id']
            if o_id not in order_items:
                order_items[o_id] = []
            order_items[o_id].append(f"{item['quantity']}x {item['name']}")
    conn.close()

    if not active_orders:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:40px;">
            <div style="width:40px; height:40px; border-radius:50%; background:rgba(34,197,94,0.1);
                display:flex; align-items:center; justify-content:center; margin:0 auto 12px;
                border:1px solid rgba(34,197,94,0.1);">
                <span style="color:#22C55E; font-weight:600; font-size:0.9rem;">&#10003;</span>
            </div>
            <h3 style="color:#22C55E; margin:0 0 4px;">All Clear</h3>
            <p style="color:#71717A; font-size:0.85rem; margin:0;">No pending orders. The kitchen is caught up.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    col_pending, col_preparing = st.columns(2)

    with col_pending:
        st.markdown("<h4 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin-bottom:16px;'>Incoming Tickets</h4>", unsafe_allow_html=True)
        pending_list = [o for o in active_orders if o['status'] == 'pending']
        if not pending_list:
            st.markdown("<p style='color:#71717A; font-size:0.85rem;'>No incoming tickets.</p>", unsafe_allow_html=True)
        for order in pending_list:
            o_id = order['id']
            table = order['table_number']
            served = order.get('served_by', 'N/A') or 'N/A'
            items_list = order_items.get(o_id, [])
            try:
                elapsed = datetime.now() - datetime.fromisoformat(order['created_at'])
                elapsed_min = int(elapsed.total_seconds() / 60)
                if elapsed_min < 3:
                    aging_class = "badge-low"
                    aging_label = f"Fresh ({elapsed_min}m)"
                elif elapsed_min < 10:
                    aging_class = "badge-medium"
                    aging_label = f"Aging ({elapsed_min}m)"
                else:
                    aging_class = "badge-critical"
                    aging_label = f"STALE ({elapsed_min}m)"
            except Exception:
                aging_class = "badge-low"
                aging_label = "New"

            st.markdown(f"""
            <div class="glass-card" style="padding:16px; margin-bottom:12px; border-left:3px solid #3B82F6;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#FAFAFA; font-size:0.9rem;">Order #{o_id}</strong>
                    <span class="badge badge-blue">{table or 'Takeout'}</span>
                </div>
                <div style="margin: 8px 0; font-size:0.85rem; color:#A1A1AA;">
                    {', '.join(items_list)}
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                    <span style="font-size:0.75rem; color:#71717A;">Served by: {served}</span>
                    <span class="badge {aging_class}">{aging_label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Start Cooking", key=f"cook_{o_id}", use_container_width=True):
                    update_order_status(o_id, 'preparing')
                    st.rerun()
            with c2:
                if st.button("Cancel", key=f"cancel_p_{o_id}", use_container_width=True):
                    restore_stock(o_id)
                    update_order_status(o_id, 'voided')
                    st.warning(f"Order #{o_id} voided. Stock restored.")
                    st.rerun()

    with col_preparing:
        st.markdown("<h4 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin-bottom:16px;'>In Preparation</h4>", unsafe_allow_html=True)
        preparing_list = [o for o in active_orders if o['status'] == 'preparing']
        if not preparing_list:
            st.markdown("<p style='color:#71717A; font-size:0.85rem;'>Nothing cooking right now.</p>", unsafe_allow_html=True)
        for order in preparing_list:
            o_id = order['id']
            table = order['table_number']
            served = order.get('served_by', 'N/A') or 'N/A'
            items_list = order_items.get(o_id, [])
            try:
                elapsed = datetime.now() - datetime.fromisoformat(order['created_at'])
                elapsed_min = int(elapsed.total_seconds() / 60)
                if elapsed_min < 15:
                    aging_class = "badge-low"
                    aging_label = f"Cooking ({elapsed_min}m)"
                elif elapsed_min < 25:
                    aging_class = "badge-medium"
                    aging_label = f"Taking Long ({elapsed_min}m)"
                else:
                    aging_class = "stale-badge"
                    aging_label = f"SLOW ({elapsed_min}m)"
            except Exception:
                aging_class = "badge-low"
                aging_label = "Cooking"

            st.markdown(f"""
            <div class="glass-card" style="padding:16px; margin-bottom:12px; border-left:3px solid #C9A86A;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#FAFAFA; font-size:0.9rem;">Order #{o_id}</strong>
                    <span class="badge badge-gold">{table or 'Takeout'}</span>
                </div>
                <div style="margin: 8px 0; font-size:0.85rem; color:#A1A1AA;">
                    {', '.join(items_list)}
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px;">
                    <span style="font-size:0.75rem; color:#71717A;">Served by: {served}</span>
                    <span class="badge {aging_class}">{aging_label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Serve", key=f"serve_{o_id}", use_container_width=True):
                    update_order_status(o_id, 'completed')
                    st.success(f"Order #{o_id} served!")
                    st.rerun()
            with c2:
                if st.button("Void", key=f"void_{o_id}", use_container_width=True):
                    restore_stock(o_id)
                    alert_id = check_void_anomaly(
                        order_id=o_id,
                        staff_username=user["username"],
                        current_status='preparing'
                    )
                    update_order_status(o_id, 'voided')
                    st.error(f"Order #{o_id} voided! Security alert triggered.")
                    st.rerun()
