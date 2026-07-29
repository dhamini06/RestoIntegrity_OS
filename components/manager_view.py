import streamlit as st
import sqlite3
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import get_db_connection
from integrity_engine import check_void_anomaly, check_discount_anomaly, check_shrinkage_anomaly
from gemini_service import get_demand_forecast, ask_manager_assistant

AXIS_STYLE = dict(gridcolor='rgba(255,255,255,0.04)', zerolinecolor='rgba(255,255,255,0.04)')

DARK_TEMPLATE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_family='Manrope, sans-serif',
    font_color='#A1A1AA',
    hovermode='x unified',
    hoverlabel=dict(bgcolor='#1F1F23', font_color='#FAFAFA', font_family='Manrope', font_size=12),
    margin=dict(l=0, r=0, t=40, b=0),
    legend=dict(font=dict(color='#71717A')),
    title=dict(font=dict(color='#FAFAFA', size=14, family='Manrope', weight=700))
)

GOLD = '#C9A86A'
BLUE = '#3B82F6'
EMERALD = '#22C55E'
AMBER = '#F59E0B'
ROSE = '#EF4444'

def render_manager_view(user):
    st.markdown("<h2 style='font-weight:700; color:#FAFAFA; font-size:1.4rem; margin-bottom:4px;'>Operations Command Center</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#71717A; font-size:0.85rem; margin-bottom:24px;'>Business intelligence, anomaly detection, and AI-powered insights.</p>", unsafe_allow_html=True)

    tab_sec, tab_analytics, tab_tips, tab_copilot = st.tabs([
        "Operations Hub",
        "Revenue Analytics",
        "Tips & Staff",
        "AI Business Advisor"
    ])

    with tab_sec:
        render_security_feed(user)
    with tab_analytics:
        render_analytics()
    with tab_tips:
        render_tips_dashboard()
    with tab_copilot:
        render_ai_copilot()


def render_security_feed(user):
    st.markdown("""
    <div class="glass-card" style="margin-bottom:24px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:16px;">
            <div style="width:6px; height:6px; border-radius:50%; background:#22C55E; box-shadow: 0 0 8px rgba(34,197,94,0.3);"></div>
            <span style="font-size:0.85rem; color:#A1A1AA; font-weight:500;">Live Operations Feed</span>
        </div>
        <p style="color:#71717A; font-size:0.8rem; margin:0;">Monitor anomalies, low stock alerts, and system health.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin-bottom:12px;'>Scenario Simulator</h4>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.popover("High Cancellation Day", use_container_width=True):
            st.markdown("<p style='color:#71717A; font-size:0.82rem;'>Simulates a day with multiple order cancellations.</p>", unsafe_allow_html=True)
            if st.button("Run Simulation", key="confirm_void", use_container_width=True):
                simulate_void_anomaly()
                st.success("High cancellation scenario created!")
                st.rerun()
    with c2:
        with st.popover("Discount Spike", use_container_width=True):
            st.markdown("<p style='color:#71717A; font-size:0.82rem;'>Simulates unusual discount patterns.</p>", unsafe_allow_html=True)
            if st.button("Run Simulation", key="confirm_disc", use_container_width=True):
                simulate_discount_anomaly()
                st.success("Discount spike scenario created!")
                st.rerun()
    with c3:
        with st.popover("Stock Depletion Alert", use_container_width=True):
            st.markdown("<p style='color:#71717A; font-size:0.82rem;'>Simulates a low stock scenario.</p>", unsafe_allow_html=True)
            if st.button("Run Simulation", key="confirm_shrink", use_container_width=True):
                simulate_shrinkage_anomaly()
                st.success("Stock depletion alert triggered!")
                st.rerun()

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    check_low_stock_alerts()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM security_alerts ORDER BY id DESC")
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()

    if not alerts:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:32px;">
            <div style="width:40px; height:40px; border-radius:50%; background:rgba(34,197,94,0.1);
                display:flex; align-items:center; justify-content:center; margin:0 auto 12px;
                border:1px solid rgba(34,197,94,0.1);">
                <span style="color:#22C55E; font-weight:600; font-size:0.9rem;">&#10003;</span>
            </div>
            <p style="color:#22C55E; font-weight:600; margin:0;">All clear! No operational alerts.</p>
            <p style="color:#71717A; font-size:0.8rem; margin-top:4px;">System is operating normally.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    for alert in alerts:
        a_id = alert['id']
        sev = alert['severity']
        a_type = alert['alert_type']
        triggered_by = alert['triggered_by'] or "system"
        details = json.loads(alert['details'])
        status = alert['status']

        card_class = {"high": "alert-card-high", "medium": "alert-card-medium"}.get(sev, "alert-card-low")
        badge_class = {"high": "badge-critical", "medium": "badge-medium"}.get(sev, "badge-low")
        label_map = {
            "void_anomaly": "High Cancellation Rate",
            "discount_anomaly": "Unusual Discount Pattern",
            "shrinkage_anomaly": "Stock Depletion Warning"
        }
        display_name = label_map.get(a_type, a_type)

        status_colors = {"active": "badge-critical", "investigated": "badge-medium", "resolved": "badge-low"}
        status_badge = status_colors.get(status, "badge-low")

        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#FAFAFA; font-size:0.9rem;">{display_name} <span style="color:#71717A; font-weight:400;">#{a_id}</span></strong>
                <div>
                    <span class="badge {status_badge}">{status.upper()}</span>
                    <span class="badge {badge_class}" style="margin-left:4px;">{sev}</span>
                </div>
            </div>
            <div style="font-size:0.78rem; margin-top:8px; color:#71717A;">
                By <b style="color:#A1A1AA;">{triggered_by}</b> &mdash; {alert['created_at'][:16]}
            </div>
            <p style="margin: 8px 0 0; font-size:0.85rem; color:#A1A1AA; font-style:italic;">
                &ldquo;{details.get('reason', 'System flagged discrepancy')}&rdquo;
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"Details & Analysis &mdash; Alert #{a_id}"):
            col_det, col_ai = st.columns(2)
            with col_det:
                st.markdown("<p style='color:#FAFAFA; font-weight:600; font-size:0.85rem;'>Alert Details</p>", unsafe_allow_html=True)
                st.json(details)
                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if status == 'active':
                        if st.button("Investigate", key=f"inv_{a_id}", use_container_width=True):
                            update_alert_status(a_id, "investigated")
                            st.rerun()
                with c2:
                    if status in ('active', 'investigated'):
                        if st.button("Resolve", key=f"res_{a_id}", use_container_width=True):
                            update_alert_status(a_id, "resolved")
                            st.rerun()

            with col_ai:
                st.markdown("<p style='color:#C9A86A; font-weight:600; font-size:0.85rem;'>AI Business Insight</p>", unsafe_allow_html=True)
                ai_raw = alert['ai_analysis']
                if ai_raw:
                    try:
                        ai_data = json.loads(ai_raw)
                        st.markdown(f"<span style='color:#A1A1AA; font-size:0.82rem;'>Classification: <span style='color:#FAFAFA;'>{ai_data.get('threat_classification', 'N/A')}</span></span>", unsafe_allow_html=True)
                        score = ai_data.get('risk_score', 0)
                        score_color = ROSE if score >= 70 else AMBER if score >= 40 else EMERALD
                        st.markdown(f"<span style='color:#A1A1AA; font-size:0.82rem;'>Priority Score: <span style='color:{score_color}; font-weight:700;'>{score}/100</span></span>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color:#A1A1AA; font-size:0.82rem;'>Analysis: <span style='color:#FAFAFA;'>{ai_data.get('incident_summary', 'N/A')}</span></span>", unsafe_allow_html=True)
                        st.markdown("<p style='color:#A1A1AA; font-size:0.82rem; margin-bottom:4px;'>Recommended Actions:</p>", unsafe_allow_html=True)
                        for i, step in enumerate(ai_data.get('recommended_actions', [])):
                            st.markdown(f"<span style='color:#71717A; font-size:0.8rem;'>{i+1}. {step}</span>", unsafe_allow_html=True)
                    except Exception:
                        st.write(ai_raw)
                else:
                    st.markdown("<p style='color:#71717A; font-size:0.82rem;'>No AI analysis yet. Add your Gemini API key in settings to enable.</p>", unsafe_allow_html=True)


def render_analytics():
    st.markdown("<h3 style='color:#FAFAFA; font-weight:600; font-size:1.1rem; margin-bottom:16px;'>Revenue Analytics</h3>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        date_from = st.date_input("From", value=datetime.now().date() - timedelta(days=7), key="date_from")
    with c2:
        date_to = st.date_input("To", value=datetime.now().date(), key="date_to")

    date_from_str = datetime.combine(date_from, datetime.min.time()).isoformat()
    date_to_str = datetime.combine(date_to, datetime.max.time()).isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM orders WHERE status = 'completed' AND created_at BETWEEN ? AND ?",
                   (date_from_str, date_to_str))
    total_sales = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE created_at BETWEEN ? AND ?",
                   (date_from_str, date_to_str))
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM security_alerts WHERE status = 'active'")
    active_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total), 0) FROM orders WHERE status = 'voided' AND created_at BETWEEN ? AND ?",
                   (date_from_str, date_to_str))
    voided_value = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(discount), 0) FROM orders WHERE discount > 0 AND created_at BETWEEN ? AND ?",
                   (date_from_str, date_to_str))
    discount_leakage = cursor.fetchone()[0]

    conn.close()

    from components.ui_helpers import show_metric_card
    k1, k2, k3 = st.columns(3)
    with k1:
        show_metric_card("Verified Revenue", f"${total_sales:,.2f}", "", "gold")
    with k2:
        show_metric_card("Total Orders", str(total_orders), "", "emerald")
    with k3:
        show_metric_card("Active Alerts", str(active_alerts), "", "amber")

    l1, l2 = st.columns(2)
    with l1:
        show_metric_card("Cancelled Revenue", f"${voided_value:,.2f}", "", "amber")
    with l2:
        show_metric_card("Discount Spend", f"${discount_leakage:,.2f}", "", "amber")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT created_at, total FROM orders WHERE status = 'completed' AND created_at BETWEEN ? AND ?",
                   (date_from_str, date_to_str))
    sales_rows = cursor.fetchall()

    if sales_rows:
        df = pd.DataFrame([dict(r) for r in sales_rows])
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['Hour'] = df['created_at'].dt.strftime('%H:00')
        grouped = df.groupby('Hour')['total'].sum().reset_index()
        fig = px.bar(grouped, x='Hour', y='total', title='Revenue by Hour',
                     labels={'total': 'Revenue ($)', 'Hour': 'Time'},
                     template='plotly_dark')
        fig.update_traces(marker_color=GOLD, marker_line_color='rgba(201,168,106,0.3)', marker_line_width=1,
                          hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>')
        fig.update_layout(**DARK_TEMPLATE, xaxis=dict(**AXIS_STYLE, dtick=1),
                          yaxis=dict(**AXIS_STYLE, tickprefix='$'))
        st.plotly_chart(fig, use_container_width=True)

    cursor.execute("""
        SELECT served_by as staff, COUNT(*) as total_orders,
               SUM(CASE WHEN status = 'voided' THEN 1 ELSE 0 END) as voided
        FROM orders WHERE served_by IS NOT NULL
        GROUP BY served_by
    """)
    staff_data = [dict(r) for r in cursor.fetchall()]
    if staff_data:
        df_staff = pd.DataFrame(staff_data)
        df_staff['void_rate'] = (df_staff['voided'] / df_staff['total_orders'] * 100).round(1)
        fig2 = px.bar(df_staff, x='staff', y='void_rate', title='Cancellation Rate by Staff',
                      labels={'void_rate': 'Cancel %', 'staff': 'Employee'},
                      template='plotly_dark', color='void_rate',
                      color_continuous_scale=[EMERALD, AMBER, ROSE])
        fig2.update_traces(hovertemplate='<b>%{x}</b><br>Cancel Rate: %{y}%<extra></extra>')
        fig2.update_layout(**DARK_TEMPLATE, coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    cursor.execute("SELECT id, discount_applied_by, discount, subtotal, created_at FROM orders WHERE discount > 0")
    disc_rows = [dict(r) for r in cursor.fetchall()]
    if disc_rows:
        df_disc = pd.DataFrame(disc_rows)
        df_disc['created_at'] = pd.to_datetime(df_disc['created_at'])
        df_disc['pct'] = (df_disc['discount'] / df_disc['subtotal'] * 100).round(1)
        fig3 = px.scatter(df_disc, x='created_at', y='pct', size='discount',
                          color='discount_applied_by', title='Discount Patterns Over Time',
                          labels={'pct': 'Discount %', 'created_at': 'Date', 'discount_applied_by': 'Staff'},
                          template='plotly_dark',
                          color_discrete_sequence=[GOLD, BLUE, EMERALD, AMBER])
        fig3.update_traces(hovertemplate='<b>%{x}</b><br>Discount: %{y}%<br>By: %{customdata}<extra></extra>')
        fig3.update_layout(**DARK_TEMPLATE)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<h3 style='color:#FAFAFA; font-weight:600; font-size:1.1rem; margin:24px 0 16px;'>Item Performance</h3>", unsafe_allow_html=True)

    cursor.execute("""
        SELECT mi.name, mi.category,
               SUM(oi.quantity) as units_sold,
               SUM(oi.quantity * oi.unit_price) as item_revenue
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE o.status = 'completed' AND o.created_at BETWEEN ? AND ?
        GROUP BY mi.name
        ORDER BY units_sold DESC
    """, (date_from_str, date_to_str))
    item_rows = [dict(r) for r in cursor.fetchall()]

    if item_rows:
        df_items = pd.DataFrame(item_rows)

        ip1, ip2 = st.columns([3, 2])

        with ip1:
            fig_items = px.bar(df_items, x='name', y='units_sold', color='category',
                               title='Units Sold by Item',
                               labels={'units_sold': 'Units Sold', 'name': 'Item'},
                               template='plotly_dark',
                               color_discrete_sequence=[GOLD, BLUE, EMERALD, AMBER])
            fig_items.update_traces(hovertemplate='<b>%{x}</b><br>Sold: %{y}<br>%{customdata}<extra></extra>')
            fig_items.update_layout(**DARK_TEMPLATE, xaxis_tickangle=-30, showlegend=False)
            st.plotly_chart(fig_items, use_container_width=True)

        with ip2:
            fig_rev = px.pie(df_items, values='item_revenue', names='name',
                             title='Revenue Share by Item',
                             template='plotly_dark',
                             color_discrete_sequence=[GOLD, '#D4B47A', '#A88A4A', '#8B6F3A', '#6D5530', '#504020'])
            fig_rev.update_layout(**DARK_TEMPLATE, showlegend=False)
            fig_rev.update_traces(textinfo='percent+label', textfont_color='#FAFAFA', textfont_size=11, textfont_family='Manrope',
                                  hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>')
            st.plotly_chart(fig_rev, use_container_width=True)

        best = df_items.iloc[0]
        worst = df_items.iloc[-1]
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            show_metric_card("Top Seller", f"{best['name']}", "", "gold")
        with ic2:
            show_metric_card("Top Revenue", f"${best['item_revenue']:,.2f}", "", "gold")
        with ic3:
            show_metric_card("Lowest Seller", f"{worst['name']}", "", "amber")

        st.markdown("<div class='glass-card' style='padding:0; overflow:hidden;'>", unsafe_allow_html=True)
        st.dataframe(df_items.rename(columns={
            'name': 'Item', 'category': 'Category',
            'units_sold': 'Units Sold', 'item_revenue': 'Revenue ($)'
        }), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#71717A; font-size:0.85rem;'>No completed orders in this date range.</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:#FAFAFA; font-weight:600; font-size:1.1rem; margin:24px 0 16px;'>Time Patterns</h3>", unsafe_allow_html=True)

    cursor.execute("""
        SELECT created_at FROM orders WHERE status = 'completed'
    """)
    time_rows = cursor.fetchall()

    if time_rows:
        df_time = pd.DataFrame([dict(r) for r in time_rows])
        df_time['created_at'] = pd.to_datetime(df_time['created_at'])
        df_time['hour'] = df_time['created_at'].dt.hour
        df_time['day_name'] = df_time['created_at'].dt.day_name()
        df_time['day_num'] = df_time['created_at'].dt.dayofweek

        hourly_counts = df_time.groupby('hour').size().reset_index(name='orders')
        all_hours = pd.DataFrame({'hour': range(24)})
        hourly_counts = all_hours.merge(hourly_counts, on='hour', how='left').fillna(0)
        hourly_counts['orders'] = hourly_counts['orders'].astype(int)

        tp1, tp2 = st.columns([3, 2])

        with tp1:
            fig_hourly = px.bar(hourly_counts, x='hour', y='orders',
                                title='Orders by Hour of Day',
                                labels={'orders': 'Number of Orders', 'hour': 'Hour'},
                                template='plotly_dark')
            fig_hourly.update_traces(
                marker_color=[GOLD if v < hourly_counts['orders'].quantile(0.75)
                              else BLUE if v >= hourly_counts['orders'].quantile(0.9)
                              else '#D4B47A' for v in hourly_counts['orders']],
                hovertemplate='<b>%{x}:00</b><br>Orders: %{y}<extra></extra>'
            )
            fig_hourly.update_layout(**DARK_TEMPLATE, xaxis=dict(**AXIS_STYLE, dtick=2))
            st.plotly_chart(fig_hourly, use_container_width=True)

        peak_hour = int(hourly_counts.loc[hourly_counts['orders'].idxmax(), 'hour'])
        quiet_hour = int(hourly_counts.loc[hourly_counts['orders'].idxmin(), 'hour'])
        peak_day = df_time.groupby('day_name').size().idxmax()

        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            show_metric_card("Peak Hour", f"{peak_hour:02d}:00", "", "gold")
        with tc2:
            show_metric_card("Quietest Hour", f"{quiet_hour:02d}:00", "", "amber")
        with tc3:
            show_metric_card("Busiest Day", f"{peak_day}", "", "gold")

        with tp2:
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily = df_time.groupby('day_name').size().reindex(day_order).fillna(0).reset_index()
            daily.columns = ['day', 'orders']
            daily['orders'] = daily['orders'].astype(int)
            fig_daily = px.bar(daily, x='day', y='orders',
                               title='Orders by Day of Week',
                               labels={'orders': 'Orders', 'day': 'Day'},
                               template='plotly_dark')
            fig_daily.update_traces(marker_color=GOLD,
                                    hovertemplate='<b>%{x}</b><br>Orders: %{y}<extra></extra>')
            fig_daily.update_layout(**DARK_TEMPLATE, xaxis_tickangle=-30)
            st.plotly_chart(fig_daily, use_container_width=True)

        st.markdown("<h4 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin-bottom:12px;'>Weekly Heatmap</h4>", unsafe_allow_html=True)
        pivot = df_time.groupby(['day_name', 'hour']).size().reset_index(name='orders')
        heatmap_data = pivot.pivot(index='day_name', columns='hour', values='orders').fillna(0)
        heatmap_data = heatmap_data.reindex([d for d in day_order if d in heatmap_data.index])

        fig_heat = px.imshow(heatmap_data, labels=dict(x="Hour", y="Day", color="Orders"),
                             title="Order Volume Heatmap",
                             template='plotly_dark',
                             color_continuous_scale=['#09090B', '#1F1F23', GOLD])
        fig_heat.update_layout(**DARK_TEMPLATE, xaxis=dict(dtick=2), coloraxis_showscale=False)
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown(f"""
        <div class="glass-card" style="background:#1A1810; border-color:rgba(201,168,106,0.1);">
            <p style="color:#C9A86A; font-size:0.85rem; margin:0; font-weight:500;">
                &#9889; Peak operations at <strong>{peak_hour:02d}:00</strong> on <strong>{peak_day}s</strong>. Consider scheduling extra staff during peak hours.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#71717A; font-size:0.85rem;'>No completed order data available for time pattern analysis.</p>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:#FAFAFA; font-weight:600; font-size:1.1rem; margin:24px 0 16px;'>Ingredient Inventory</h3>", unsafe_allow_html=True)
    cursor.execute("SELECT item_name, current_quantity, min_threshold, unit, last_updated FROM inventory")
    inv_rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if inv_rows:
        df_inv = pd.DataFrame(inv_rows)
        st.markdown("<div class='glass-card' style='padding:0; overflow:hidden;'>", unsafe_allow_html=True)
        st.dataframe(df_inv.rename(columns={
            'item_name': 'Ingredient', 'current_quantity': 'Stock',
            'min_threshold': 'Threshold', 'unit': 'Unit', 'last_updated': 'Last Updated'
        }), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin:20px 0 12px;'>AI Stockout Forecast</h4>", unsafe_allow_html=True)
        sel = st.selectbox("", [r['item_name'] for r in inv_rows], key="forecast_sel", label_visibility="collapsed", placeholder="Select ingredient...")
        if st.button("Forecast Depletion", use_container_width=True):
            item_data = next((r for r in inv_rows if r['item_name'] == sel), None)
            if item_data:
                with st.spinner("Analyzing..."):
                    fc = get_demand_forecast(sel, item_data['current_quantity'])
                fc1, fc2 = st.columns([1, 2])
                with fc1:
                    st.markdown(f"<span style='color:#A1A1AA; font-size:0.85rem;'>Days to Stockout: <span style='color:#FAFAFA; font-weight:600;'>{fc.get('predicted_runout_days')}</span></span>", unsafe_allow_html=True)
                    risk = fc.get('risk_level', '')
                    risk_color = ROSE if 'high' in risk.lower() else AMBER if 'medium' in risk.lower() else EMERALD
                    st.markdown(f"<span style='color:#A1A1AA; font-size:0.85rem;'>Risk: <span style='color:{risk_color}; font-weight:600;'>{risk}</span></span>", unsafe_allow_html=True)
                with fc2:
                    st.markdown(f"<div class='glass-card-subtle' style='padding:12px;'><p style='color:#A1A1AA; font-size:0.82rem; margin:0;'>{fc.get('explanation', '')}</p></div>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin:20px 0 12px;'>Physical Stock Count</h4>", unsafe_allow_html=True)
        uc1, uc2, uc3 = st.columns(3)
        with uc1:
            up_item = st.selectbox("", [r['item_name'] for r in inv_rows], key="up_item", label_visibility="collapsed", placeholder="Select ingredient...")
        with uc2:
            up_qty = st.number_input("", min_value=0.0, max_value=200.0, step=1.0, label_visibility="collapsed", placeholder="Physical count")
        with uc3:
            if st.button("Submit Count", use_container_width=True):
                alert_id = check_shrinkage_anomaly(up_item, up_qty, "admin")
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("UPDATE inventory SET current_quantity = ?, last_updated = ? WHERE item_name = ?",
                               (up_qty, datetime.now().isoformat(), up_item))
                conn.commit()
                conn.close()
                if alert_id:
                    st.error(f"Discrepancy alert #{alert_id} triggered!")
                else:
                    st.success("Inventory verified.")


def render_tips_dashboard():
    st.markdown("<h3 style='color:#FAFAFA; font-weight:600; font-size:1.1rem; margin-bottom:16px;'>Tips & Waiter Earnings</h3>", unsafe_allow_html=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COALESCE(SUM(tip), 0) FROM orders WHERE status = 'completed'")
    total_tips = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(AVG(tip), 0) FROM orders WHERE status = 'completed' AND tip > 0")
    avg_tip = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed' AND tip > 0")
    tipped_orders = cursor.fetchone()[0]

    from components.ui_helpers import show_metric_card
    k1, k2, k3 = st.columns(3)
    with k1:
        show_metric_card("Total Tips Collected", f"${total_tips:,.2f}", "", "gold")
    with k2:
        show_metric_card("Average Tip", f"${avg_tip:,.2f}", "", "gold")
    with k3:
        show_metric_card("Orders with Tips", str(tipped_orders), "", "emerald")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    cursor.execute("""
        SELECT served_by,
               COUNT(*) as total_orders,
               SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
               COALESCE(SUM(CASE WHEN status = 'completed' THEN tip ELSE 0 END), 0) as total_tips,
               COALESCE(AVG(CASE WHEN status = 'completed' AND tip > 0 THEN tip END), 0) as avg_tip,
               COALESCE(SUM(CASE WHEN status = 'completed' THEN total ELSE 0 END), 0) as total_revenue
        FROM orders WHERE served_by IS NOT NULL
        GROUP BY served_by
    """)
    waiter_data = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if waiter_data:
        df_w = pd.DataFrame(waiter_data)
        df_w['tip_pct'] = ((df_w['total_tips'] / df_w['total_revenue'].replace(0, 1)) * 100).round(1)

        fig = px.bar(df_w, x='served_by', y='total_tips',
                     title='Total Tips by Waiter',
                     labels={'total_tips': 'Tips ($)', 'served_by': 'Waiter'},
                     template='plotly_dark',
                     color='total_tips',
                     color_continuous_scale=[AMBER, GOLD])
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Tips: $%{y:,.2f}<extra></extra>')
        fig.update_layout(**DARK_TEMPLATE, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<h4 style='color:#A1A1AA; font-weight:600; font-size:0.9rem; margin-bottom:12px;'>Waiter Breakdown</h4>", unsafe_allow_html=True)
        for w in waiter_data:
            tips = w['total_tips']
            completed = w['completed_orders']
            total = w['total_orders']
            avg = w['avg_tip']
            st.markdown(f"""
            <div class="glass-card" style="padding:16px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="color:#FAFAFA; font-size:0.95rem;">{w['served_by']}</strong>
                    <div style="font-size:0.78rem; color:#71717A; margin-top:2px;">
                        {completed}/{total} orders completed
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.3rem; font-weight:700; color:#22C55E;">${tips:.2f}</div>
                    <div style="font-size:0.75rem; color:#71717A;">avg ${avg:.2f}/order</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT created_at, tip, served_by FROM orders WHERE tip > 0 AND status = 'completed'")
        tip_rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        if tip_rows:
            df_tips = pd.DataFrame(tip_rows)
            df_tips['created_at'] = pd.to_datetime(df_tips['created_at'])
            fig2 = px.scatter(df_tips, x='created_at', y='tip', color='served_by',
                              size='tip', title='Tips Over Time',
                              labels={'tip': 'Tip ($)', 'created_at': 'Date', 'served_by': 'Waiter'},
                              template='plotly_dark',
                              color_discrete_sequence=[GOLD, BLUE, EMERALD, AMBER, ROSE])
            fig2.update_traces(hovertemplate='<b>%{x}</b><br>Tip: $%{y:.2f}<br>%{customdata}<extra></extra>')
            fig2.update_layout(**DARK_TEMPLATE, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)


def render_ai_copilot():
    st.markdown("<h3 style='color:#FAFAFA; font-weight:600; font-size:1.1rem; margin-bottom:4px;'>AI Business Advisor</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#71717A; font-size:0.82rem; margin-bottom:20px;'>Ask about sales trends, inventory, tips, or operational patterns.</p>", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for role, text in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(f"<div class='glass-card-subtle' style='padding:12px; margin-bottom:4px;'><p style='color:#FAFAFA; font-size:0.85rem; margin:0;'>{text}</p></div>", unsafe_allow_html=True)

    chips = ["Audit Bob's voids", "What's low on stock?", "Show tip earnings", "Draft a restock list"]
    cols = st.columns(len(chips))
    for col, chip_text in zip(cols, chips):
        with col:
            if st.button(chip_text, use_container_width=True):
                st.session_state.messages.append(("user", chip_text))
                with st.spinner("Thinking..."):
                    res = ask_manager_assistant(st.session_state.messages[:-1], chip_text)
                st.session_state.messages.append(("assistant", res))
                st.rerun()

    if prompt := st.chat_input("Ask about sales, inventory, tips..."):
        st.session_state.messages.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(f"<div class='glass-card-subtle' style='padding:12px; margin-bottom:4px;'><p style='color:#FAFAFA; font-size:0.85rem; margin:0;'>{prompt}</p></div>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                res = ask_manager_assistant(st.session_state.messages[:-1], prompt)
            st.markdown(f"<div class='glass-card-subtle' style='padding:12px; margin-bottom:4px;'><p style='color:#FAFAFA; font-size:0.85rem; margin:0;'>{res}</p></div>", unsafe_allow_html=True)
            st.session_state.messages.append(("assistant", res))
            st.rerun()


def update_alert_status(alert_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE security_alerts SET status = ? WHERE id = ?", (status, alert_id))
    conn.commit()
    conn.close()


def check_low_stock_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, current_quantity, min_threshold, unit FROM inventory WHERE current_quantity <= min_threshold")
    low_items = [dict(row) for row in cursor.fetchall()]
    if low_items:
        items_str = ", ".join([f"**{i['item_name']}** ({i['current_quantity']}{i.get('unit', '')})" for i in low_items])
        st.warning(f"Low stock alert: {items_str}")
    conn.close()


def simulate_void_anomaly():
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    prepping_str = (datetime.now() - timedelta(minutes=10)).isoformat()
    cursor.execute(
        "INSERT INTO orders (table_number, status, subtotal, discount, total, tax, tip, payment_method, served_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("Table 2", "preparing", 53.0, 0.0, 53.0, 4.64, 10.60, "Cash", "bob", now_str)
    )
    order_id = cursor.lastrowid
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 3, 1, 45.0))
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 6, 1, 8.0))
    conn.commit()
    conn.close()
    check_void_anomaly(order_id, "bob", "preparing")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'voided' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def simulate_discount_anomaly():
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO orders (table_number, status, subtotal, discount, total, tax, tip, payment_method, discount_applied_by, served_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("Table 3", "completed", 90.0, 45.0, 57.38, 7.88, 9.0, "Cash", "bob", "alice", now_str)
    )
    order_id = cursor.lastrowid
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 2, 2, 18.0))
    cursor.execute("INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_id, 3, 1, 45.0))
    conn.commit()
    conn.close()
    check_discount_anomaly(order_id, "bob", 45.0)

def simulate_shrinkage_anomaly():
    check_shrinkage_anomaly("Potatoes", 10.0, "chef_ramsay")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET current_quantity = 10.0, last_updated = ? WHERE item_name = 'Potatoes'",
                   (datetime.now().isoformat(),))
    conn.commit()
    conn.close()
