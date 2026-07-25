import streamlit as st
import sqlite3
from database import get_db_connection
from integrity_engine import check_void_anomaly
from datetime import datetime

def render_kitchen_view():
    st.markdown("<h2 class='glow-text-purple'>👨‍🍳 Kitchen Order Dispatcher</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#a0aec0;'>Manage live preparation queues and coordinate status pushes to tables.</p>", unsafe_allow_html=True)

    # Active kitchen staff selector
    if "kitchen_staff" not in st.session_state:
        st.session_state.kitchen_staff = "chef_ramsay"
        
    st.session_state.kitchen_staff = st.selectbox(
        "Active Kitchen Operator:",
        ["chef_ramsay", "alice", "bob"]
    )
    
    # Fetch active orders
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.table_number, o.status, o.subtotal, o.created_at
        FROM orders o
        WHERE o.status IN ('pending', 'preparing')
        ORDER BY o.id ASC
    """)
    active_orders = [dict(row) for row in cursor.fetchall()]
    
    # Fetch items for active orders
    order_items = {}
    if active_orders:
        order_ids = [str(o['id']) for o in active_orders]
        query = f"""
            SELECT oi.order_id, oi.quantity, mi.name 
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id IN ({','.join(order_ids)})
        """
        cursor.execute(query)
        items = cursor.fetchall()
        for item in items:
            o_id = item['order_id']
            if o_id not in order_items:
                order_items[o_id] = []
            order_items[o_id].append(f"{item['quantity']}x {item['name']}")
            
    conn.close()

    if not active_orders:
        st.success("🎉 All orders cleared! The queue is empty.")
        return
        
    # Render orders grid
    col_pending, col_preparing = st.columns(2)
    
    with col_pending:
        st.markdown("### 📥 Incoming (Pending)")
        pending_list = [o for o in active_orders if o['status'] == 'pending']
        if not pending_list:
            st.write("No incoming tickets.")
        else:
            for order in pending_list:
                o_id = order['id']
                table = order['table_number']
                time_str = order['created_at']
                items_list = order_items.get(o_id, [])
                
                # Format time elapsed
                try:
                    elapsed = datetime.now() - datetime.fromisoformat(time_str)
                    elapsed_min = int(elapsed.total_seconds() / 60)
                    elapsed_display = f"{elapsed_min} mins ago"
                except Exception:
                    elapsed_display = "Recent"
                
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); padding:15px; border-radius:10px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between;">
                        <strong>Order #{o_id}</strong>
                        <span class="badge badge-medium">{table}</span>
                    </div>
                    <div style="margin: 8px 0; font-size:0.9rem; color:#cbd5e0;">
                        {', '.join(items_list)}
                    </div>
                    <div style="font-size:0.75rem; color:#718096; margin-bottom:10px;">
                        Received: {elapsed_display}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"🔥 Start Cooking", key=f"cook_{o_id}", width="stretch"):
                        update_order_status(o_id, 'preparing')
                        st.success(f"Order #{o_id} moved to Preparing!")
                        st.rerun()
                with col_btn2:
                    if st.button(f"❌ Cancel", key=f"cancel_pending_{o_id}", width="stretch"):
                        # Cancel order directly (doesn't trigger high anomaly since it wasn't cooked yet)
                        update_order_status(o_id, 'voided')
                        st.warning(f"Order #{o_id} voided.")
                        st.rerun()

    with col_preparing:
        st.markdown("### 🔥 In Preparation")
        preparing_list = [o for o in active_orders if o['status'] == 'preparing']
        if not preparing_list:
            st.write("No tickets being cooked.")
        else:
            for order in preparing_list:
                o_id = order['id']
                table = order['table_number']
                time_str = order['created_at']
                items_list = order_items.get(o_id, [])
                
                try:
                    elapsed = datetime.now() - datetime.fromisoformat(time_str)
                    elapsed_min = int(elapsed.total_seconds() / 60)
                    elapsed_display = f"{elapsed_min} mins ago"
                except Exception:
                    elapsed_display = "Recent"
                    
                st.markdown(f"""
                <div style="background:rgba(185,39,252,0.03); border:1px solid rgba(185,39,252,0.1); padding:15px; border-radius:10px; margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between;">
                        <strong>Order #{o_id}</strong>
                        <span class="badge badge-low">{table}</span>
                    </div>
                    <div style="margin: 8px 0; font-size:0.9rem; color:#cbd5e0;">
                        {', '.join(items_list)}
                    </div>
                    <div style="font-size:0.75rem; color:#718096; margin-bottom:10px;">
                        Cook Time: {elapsed_display}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button(f"✅ Ready / Serve", key=f"serve_{o_id}", width="stretch"):
                        update_order_status(o_id, 'completed')
                        st.success(f"Order #{o_id} completed and served!")
                        st.rerun()
                with col_btn2:
                    if st.button(f"❌ Cancel / Void", key=f"cancel_preparing_{o_id}", width="stretch"):
                        # CRITICAL SECURITY ANOMALY TRIGGER
                        # Voiding a completed or preparing order creates a security alert!
                        alert_id = check_void_anomaly(
                            order_id=o_id,
                            staff_username=st.session_state.kitchen_staff,
                            current_status='preparing'
                        )
                        update_order_status(o_id, 'voided')
                        st.error(f"Order #{o_id} voided! Security Anomaly alert triggered.")
                        st.toast("Void Alert logged to security feed!", icon="⚠️")
                        st.rerun()

def update_order_status(order_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()
