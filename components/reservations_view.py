import streamlit as st
import sqlite3
from database import get_db_connection, add_notification
from datetime import datetime, timedelta

def render_reservation_view(user):
    st.markdown("<h2 style='font-weight:700; color:#FAFAFA; font-size:1.4rem; margin-bottom:4px;'>Reservations</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#71717A; font-size:0.85rem; margin-bottom:20px;'>Book tables, manage reservations, and track dining schedules.</p>", unsafe_allow_html=True)

    is_manager = user["role"] in ("admin", "staff")
    tab_book, tab_manage = st.tabs(["Book a Table", "Manage Reservations"] if is_manager else ["Book a Table", "My Reservations"])

    with tab_book:
        render_booking_form(user)

    with tab_manage:
        if is_manager:
            render_reservation_management(user)
        else:
            render_customer_reservations(user)


def render_booking_form(user):
    st.markdown("<div class='glass-card' style='max-width:600px;'>", unsafe_allow_html=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, table_number, capacity FROM restaurant_tables ORDER BY table_number")
    tables = [dict(r) for r in cursor.fetchall()]

    d1, d2 = st.columns(2)
    with d1:
        date_val = st.date_input("Date", value=datetime.now().date() + timedelta(days=1), min_value=datetime.now().date())
    with d2:
        time_val = st.time_input("Time", value=datetime.now().time().replace(hour=19, minute=0))

    name = st.text_input("Name", placeholder="Your name", value=user.get("full_name", ""))
    email = st.text_input("Email", value=user.get("email", ""), placeholder="your@email.com")
    phone = st.text_input("Phone", placeholder="+1 (555) 000-0000")
    party_size = st.number_input("Party Size", min_value=1, max_value=20, value=2)

    reservation_dt = datetime.combine(date_val, time_val)
    available_tables = [t for t in tables if t["capacity"] >= party_size]

    if available_tables:
        table_options = {f"{t['table_number']} (Capacity: {t['capacity']})": t["id"] for t in available_tables}
        selected_table_label = st.selectbox("Preferred Table", list(table_options.keys()))
        selected_table_id = table_options[selected_table_label]
    else:
        st.warning("No tables available for this party size.")
        selected_table_id = None

    if st.button("Confirm Reservation", type="primary", use_container_width=True):
        if name and party_size > 0 and selected_table_id:
            cursor.execute(
                "INSERT INTO reservations (customer_name, customer_email, phone, party_size, table_id, reservation_time, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (name, email, phone, party_size, selected_table_id, reservation_dt.isoformat(), "confirmed", datetime.now().isoformat())
            )
            conn.commit()
            cursor.execute("UPDATE restaurant_tables SET status = 'reserved' WHERE id = ?", (selected_table_id,))
            conn.commit()
            add_notification(
                f"New Reservation: {name}",
                f"{name} booked {[t['table_number'] for t in tables if t['id'] == selected_table_id][0]} for {party_size} at {reservation_dt.strftime('%b %d, %I:%M %p')}",
                role="admin"
            )
            st.success("Reservation confirmed!")
            st.rerun()
        else:
            st.error("Please fill in all required fields.")

    conn.close()
    st.markdown("</div>", unsafe_allow_html=True)


def render_reservation_management(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, t.table_number
        FROM reservations r
        LEFT JOIN restaurant_tables t ON r.table_id = t.id
        ORDER BY r.reservation_time ASC
    """)
    reservations = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not reservations:
        st.markdown("<p style='color:#71717A; font-size:0.85rem;'>No reservations yet.</p>", unsafe_allow_html=True)
        return

    for res in reservations:
        res_time = datetime.fromisoformat(res["reservation_time"])
        status_color = {"confirmed": "badge-gold", "seated": "badge-low", "cancelled": "badge-critical"}.get(res["status"], "badge-medium")
        st.markdown(f"""
        <div class="glass-card" style="padding:16px; margin-bottom:12px; border-left:3px solid #C9A86A;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="color:#FAFAFA;">{res['customer_name']}</strong>
                    <span style="color:#71717A; font-size:0.8rem; margin-left:8px;">{res['party_size']} guests</span>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="color:#A1A1AA; font-size:0.82rem;">{res.get('table_number', 'Unassigned')}</span>
                    <span class="badge {status_color}">{res['status']}</span>
                </div>
            </div>
            <div style="color:#71717A; font-size:0.8rem; margin-top:6px;">
                {res_time.strftime('%b %d, %I:%M %p')}
            </div>
            <div style="margin-top:8px; display:flex; gap:8px;">
        """, unsafe_allow_html=True)

        if res["status"] == "confirmed":
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Seat", key=f"seat_res_{res['id']}", use_container_width=True):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("UPDATE reservations SET status = 'seated' WHERE id = ?", (res["id"],))
                    if res["table_id"]:
                        cur.execute("UPDATE restaurant_tables SET status = 'occupied' WHERE id = ?", (res["table_id"],))
                    conn.commit()
                    conn.close()
                    add_notification("Guest Seated", f"{res['customer_name']} seated at {res.get('table_number', 'assigned table')}", role="admin")
                    st.rerun()
            with c2:
                if st.button("Cancel", key=f"cancel_res_{res['id']}", use_container_width=True):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("UPDATE reservations SET status = 'cancelled' WHERE id = ?", (res["id"],))
                    if res["table_id"]:
                        cur.execute("UPDATE restaurant_tables SET status = 'available' WHERE id = ?", (res["table_id"],))
                    conn.commit()
                    conn.close()
                    st.rerun()


def render_customer_reservations(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, t.table_number
        FROM reservations r
        LEFT JOIN restaurant_tables t ON r.table_id = t.id
        WHERE r.customer_email = ?
        ORDER BY r.reservation_time DESC
    """, (user["email"],))
    reservations = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not reservations:
        st.markdown("<p style='color:#71717A; font-size:0.85rem;'>You have no reservations.</p>", unsafe_allow_html=True)
        return

    for res in reservations:
        res_time = datetime.fromisoformat(res["reservation_time"])
        status_color = {"confirmed": "badge-gold", "seated": "badge-low", "cancelled": "badge-critical"}.get(res["status"], "badge-medium")
        st.markdown(f"""
        <div class="glass-card" style="padding:14px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#FAFAFA;">{res_time.strftime('%b %d, %I:%M %p')}</strong>
                <span class="badge {status_color}">{res['status']}</span>
            </div>
            <div style="color:#71717A; font-size:0.82rem; margin-top:4px;">
                {res['party_size']} guests &middot; {res.get('table_number', 'Unassigned')}
            </div>
        </div>
        """, unsafe_allow_html=True)
