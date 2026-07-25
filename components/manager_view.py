import streamlit as st
import sqlite3
import json
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from database import get_db_connection
from integrity_engine import check_void_anomaly, check_discount_anomaly, check_shrinkage_anomaly
from gemini_service import get_demand_forecast, ask_manager_assistant

def render_manager_view():
    st.markdown("<h2 class='glow-text-cyan'>🛡️ Operational Integrity Command Center</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#a0aec0;'>Loss prevention analytics, real-time transaction guardrails, and Gemini AI forensics.</p>", unsafe_allow_html=True)

    tab_sec, tab_analytics, tab_copilot = st.tabs([
        "🚨 Security Feed (SOC Logs)", 
        "📈 Operations & Inventory Metrics", 
        "🤖 AI Loss Prevention Co-Pilot"
    ])

    with tab_sec:
        render_security_feed()

    with tab_analytics:
        render_analytics()

    with tab_copilot:
        render_ai_copilot()

def render_security_feed():
    st.markdown("### 🚨 Live Operational Alert Logs")
    
    # Simulation buttons
    st.markdown("##### ⚡ Quick Anomaly Simulations (For Judges)")
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        if st.button("Simulate Cash Skimming (Void)", use_container_width=True):
            simulate_void_anomaly()
            st.success("Simulated cash skimming event triggered!")
            st.rerun()
    with col_s2:
        if st.button("Simulate Discount Abuse", use_container_width=True):
            simulate_discount_anomaly()
            st.success("Simulated discount policy violation triggered!")
            st.rerun()
    with col_s3:
        if st.button("Simulate Inventory Loss", use_container_width=True):
            simulate_shrinkage_anomaly()
            st.success("Simulated physical inventory count mismatch!")
            st.rerun()

    st.markdown("---")
    
    # Fetch alerts
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, alert_type, severity, details, triggered_by, ai_analysis, status, created_at FROM security_alerts ORDER BY id DESC")
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    if not alerts:
        st.info("No security alerts logged. System reports 100% operational integrity.")
        return
        
    for alert in alerts:
        a_id = alert['id']
        a_type = alert['alert_type']
        sev = alert['severity']
        triggered_by = alert['triggered_by'] if alert['triggered_by'] else "system"
        time_str = alert['created_at']
        details = json.loads(alert['details'])
        
        # Display styling matching severity
        card_class = "alert-card-high" if sev == "high" else "alert-card-medium"
        badge_class = "badge-critical" if sev == "high" else "badge-medium"
        
        # Format label names
        label_map = {
            "void_anomaly": "Post-Preparation Transaction Void",
            "discount_anomaly": "High-Value Manual Discount Policy Spike",
            "shrinkage_anomaly": "Real-time Inventory Shrinkage Discrepancy"
        }
        display_name = label_map.get(a_type, a_type)
        
        # Card header HTML
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong>{display_name} (Alert #{a_id})</strong>
                <span class="badge {badge_class}">{sev} severity</span>
            </div>
            <div style="font-size:0.85rem; margin-top:8px; color:#cbd5e0;">
                Triggered by: <code>{triggered_by}</code> | Detected: {time_str}
            </div>
            <p style="margin: 8px 0 0 0; font-size:0.9rem; font-style:italic; color:#e2e8f0;">
                "{details.get('reason', 'Stock level check discrepancy')}"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Incident forensic analysis drawer
        with st.expander(f"🔍 Forensic Details & AI Investigation (Alert #{a_id})"):
            col_det, col_ai = st.columns(2)
            
            with col_det:
                st.markdown("##### 📊 Event Log Metadata")
                st.json(details)
                
                # Action buttons
                st.markdown("---")
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    if st.button("Mark Resolved", key=f"resolve_{a_id}"):
                        update_alert_status(a_id, "resolved")
                        st.success("Alert marked resolved.")
                        st.rerun()
                with col_act2:
                    if st.button("Flag for CCTV Audit", key=f"audit_{a_id}"):
                        st.info(f"CCTV request queued for timestamp {time_str}")
                        st.toast("CCTV request logged!")
                        
            with col_ai:
                st.markdown("##### 🧠 Gemini AI Forensic Report")
                ai_analysis_raw = alert['ai_analysis']
                if ai_analysis_raw:
                    try:
                        ai_data = json.loads(ai_analysis_raw)
                        st.markdown(f"**Classification:** `{ai_data.get('threat_classification', 'N/A')}`")
                        st.markdown(f"**Risk Level Score:** `{ai_data.get('risk_score', 'N/A')}/100`")
                        st.markdown(f"**Summary Analysis:**\n{ai_data.get('incident_summary', 'N/A')}")
                        st.markdown("**Actionable Audit Plan:**")
                        for idx, step in enumerate(ai_data.get('recommended_actions', [])):
                            st.markdown(f"{idx+1}. {step}")
                    except Exception:
                        st.write(ai_analysis_raw)
                else:
                    st.warning("No Gemini AI analysis available. Connect your GEMINI_API_KEY to enrich logs.")


def render_analytics():
    st.markdown("### 📈 Sales & Inventory Integrity Status")
    
    # Calculate KPIs
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(total) FROM orders WHERE status = 'completed'")
    total_sales = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM security_alerts WHERE status = 'active'")
    active_alerts = cursor.fetchone()[0] or 0
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; gap:20px; margin-bottom:20px;">
        <div class="glass-card" style="flex:1; text-align:center;">
            <div style="font-size:0.9rem; color:#cbd5e0;">Total Verified Revenue</div>
            <div class="metric-value">${total_sales:.2f}</div>
        </div>
        <div class="glass-card" style="flex:1; text-align:center;">
            <div style="font-size:0.9rem; color:#cbd5e0;">Order Count (All Channels)</div>
            <div class="metric-value">{total_orders}</div>
        </div>
        <div class="glass-card" style="flex:1; text-align:center;">
            <div style="font-size:0.9rem; color:#cbd5e0;">Active Integrity Warnings</div>
            <div class="metric-value" style="background: linear-gradient(90deg, #ff4d4d, #ff9f43); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{active_alerts}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Plotly Sales Graph
    cursor.execute("SELECT created_at, total FROM orders WHERE status = 'completed'")
    sales_rows = cursor.fetchall()
    
    if sales_rows:
        df_sales = pd.DataFrame([dict(r) for r in sales_rows])
        df_sales['created_at'] = pd.to_datetime(df_sales['created_at'])
        df_sales['Hour'] = df_sales['created_at'].dt.strftime('%H:00')
        df_grouped = df_sales.groupby('Hour')['total'].sum().reset_index()
        
        fig = px.bar(
            df_grouped, x='Hour', y='total', 
            title='Verified Sales Breakdown by Time of Day',
            labels={'total':'Revenue ($)', 'Hour':'Time Block'},
            template='plotly_dark'
        )
        fig.update_traces(marker_color='#00f2fe')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_showgrid=False,
            yaxis_showgrid=True,
            yaxis_gridcolor='rgba(255,255,255,0.05)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    # Inventory Table
    st.markdown("### 🥦 Ingredient Inventory Reconciliation")
    cursor.execute("SELECT item_name, current_quantity, min_threshold, unit, last_updated FROM inventory")
    inv_rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    if inv_rows:
        df_inv = pd.DataFrame(inv_rows)
        st.dataframe(
            df_inv.rename(columns={
                'item_name': 'Ingredient Name',
                'current_quantity': 'Stock Level',
                'min_threshold': 'Threshold Alert Limit',
                'unit': 'Unit',
                'last_updated': 'Last Checked'
            }), 
            use_container_width=True,
            hide_index=True
        )
        
        # Predictive Stockout forecasting
        st.markdown("##### 🔮 AI Stockout Demand Forecasting")
        selected_forecast_item = st.selectbox("Select ingredient for AI demand analysis:", [r['item_name'] for r in inv_rows])
        
        if st.button("Forecast Depletion Velocity"):
            item_data = next((r for r in inv_rows if r['item_name'] == selected_forecast_item), None)
            if item_data:
                with st.spinner("Analyzing depletion velocity metrics..."):
                    fc = get_demand_forecast(selected_forecast_item, item_data['current_quantity'])
                    
                col_fc1, col_fc2 = st.columns([1, 2])
                with col_fc1:
                    st.markdown(f"**Predicted Stockout:** `{fc.get('predicted_runout_days')} days`")
                    st.markdown(f"**Risk Level Assessment:** `{fc.get('risk_level')}`")
                with col_fc2:
                    st.info(fc.get('explanation'))
                    
        # Stock update tool (to trigger shrinkage manually)
        st.markdown("##### 📥 Perform Physical Stock Count Reconciliation")
        col_up1, col_up2, col_up3 = st.columns(3)
        with col_up1:
            up_item = st.selectbox("Select counted ingredient:", [r['item_name'] for r in inv_rows], key="up_item")
        with col_up2:
            up_qty = st.number_input("Physical Count quantity:", min_value=0.0, max_value=200.0, step=1.0)
        with col_up3:
            if st.button("Submit Reconciliation Count"):
                # Trigger shrinkage logic check
                alert_id = check_shrinkage_anomaly(up_item, up_qty, "admin")
                
                # Save changes
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE inventory SET current_quantity = ?, last_updated = ? WHERE item_name = ?",
                    (up_qty, datetime.now().isoformat(), up_item)
                )
                conn.commit()
                conn.close()
                
                if alert_id:
                    st.error(f"Discrepancy alert #{alert_id} triggered! Theoretical levels do not match physical count.")
                else:
                    st.success("Inventory updated and verified.")
                st.rerun()


def render_ai_copilot():
    st.markdown("### 🤖 Loss Prevention & Forensic Assistant")
    st.markdown("Ask the AI about your alerts, operational gaps, employee transaction behavior, or shrinkage metrics.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for msg_role, text in st.session_state.messages:
        with st.chat_message(msg_role):
            st.markdown(text)
            
    # Quick chips
    chips = ["Audit Bob's transaction voids", "What ingredients are below alert threshold?", "Draft a restock list for low items"]
    cols = st.columns(len(chips))
    for col, chip_text in zip(cols, chips):
        with col:
            if st.button(chip_text, use_container_width=True):
                # Add to chat
                st.session_state.messages.append(("user", chip_text))
                with st.spinner("AI is checking server audit files..."):
                    res = ask_manager_assistant(st.session_state.messages[:-1], chip_text)
                st.session_state.messages.append(("assistant", res))
                st.rerun()
                
    # Chat input
    if prompt := st.chat_input("Ask about suspicious voids, discounts, or inventory..."):
        st.session_state.messages.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("AI is checking server audit files..."):
                res = ask_manager_assistant(st.session_state.messages[:-1], prompt)
            st.markdown(res)
            st.session_state.messages.append(("assistant", res))
            st.rerun()


def update_alert_status(alert_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE security_alerts SET status = ? WHERE id = ?", (status, alert_id))
    conn.commit()
    conn.close()


# Simulators for Anomaly alerts
def simulate_void_anomaly():
    # Insert completed order, then void it
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now_str = datetime.now().isoformat()
    # 1. Insert order
    cursor.execute(
        "INSERT INTO orders (table_number, status, subtotal, discount, total, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        ("Table 2", "preparing", 53.0, 0.0, 53.0, now_str)
    )
    order_id = cursor.lastrowid
    
    # 2. Insert order items (Wagyu + Beer)
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 3, 1, 45.0))
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 6, 1, 8.0))
    
    conn.commit()
    conn.close()
    
    # 3. Cancel order through check trigger
    check_void_anomaly(order_id, "bob", "preparing")
    
    # 4. Set status to voided
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'voided' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def simulate_discount_anomaly():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now_str = datetime.now().isoformat()
    # 1. Insert order with 50% discount applied by bob
    subtotal = 90.0
    disc = 45.0
    total = 45.0
    cursor.execute(
        "INSERT INTO orders (table_number, status, subtotal, discount, total, discount_applied_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("Table 3", "completed", subtotal, disc, total, "bob", now_str)
    )
    order_id = cursor.lastrowid
    
    # 2. Insert order items (2x Miso Ramen + 1x Ribeye)
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 2, 2, 18.0))
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 3, 1, 45.0))
    
    conn.commit()
    conn.close()
    
    # 3. Audit check triggers discount anomaly
    check_discount_anomaly(order_id, "bob", disc)

def simulate_shrinkage_anomaly():
    # Force potato counts to be lower
    check_shrinkage_anomaly("Potatoes", 10.0, "chef_ramsay")
    
    # Update inventory to reflect counted value
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE inventory SET current_quantity = 10.0, last_updated = ? WHERE item_name = 'Potatoes'",
        (datetime.now().isoformat(),)
    )
    conn.commit()
    conn.close()
