import streamlit as st
from database import get_db_connection, add_notification
from datetime import datetime, timedelta

ESTIMATED_WAIT_MINUTES = {2: 10, 4: 15, 6: 20, 8: 30}

def render_queue_view(user):
    st.markdown("<h2 style='font-weight:700; color:#FAFAFA; font-size:1.4rem; margin-bottom:4px;'>Queue Management</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#71717A; font-size:0.85rem; margin-bottom:20px;'>Manage the waitlist, seat guests, and track estimated wait times.</p>", unsafe_allow_html=True)

    is_manager = user["role"] in ("admin", "staff")
    tab_join, tab_live = st.tabs(["Join Waitlist", "Live Queue"] if is_manager else ["Join Waitlist", "Queue Status"])

    with tab_join:
        render_join_queue(user)

    with tab_live:
        if is_manager:
            render_queue_dashboard(user)
        else:
            render_queue_status(user)


def render_join_queue(user):
    st.markdown("<div class='glass-card' style='max-width:500px;'>", unsafe_allow_html=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    name = st.text_input("Name", value=user.get("full_name", ""), placeholder="Your name")
    phone = st.text_input("Phone", placeholder="+1 (555) 000-0000")
    party_size = st.number_input("Party Size", min_value=1, max_value=20, value=2)

    cursor.execute("SELECT COALESCE(MAX(position), 0) FROM queue WHERE status = 'waiting'")
    next_pos = cursor.fetchone()[0] + 1

    cursor.execute("SELECT COUNT(*) FROM queue WHERE status = 'waiting'")
    ahead = cursor.fetchone()[0]

    est_min = 0
    for size, mins in sorted(ESTIMATED_WAIT_MINUTES.items()):
        if party_size <= size:
            est_min = mins * (ahead + 1)
            break
    else:
        est_min = 30 * (ahead + 1)

    if st.button("Join Waitlist", type="primary", use_container_width=True):
        if name:
            cursor.execute(
                "INSERT INTO queue (customer_name, phone, party_size, position, status, created_at) VALUES (?, ?, ?, ?, 'waiting', ?)",
                (name, phone, party_size, next_pos, datetime.now().isoformat())
            )
            conn.commit()
            add_notification(
                "New Queue Entry",
                f"{name} (party of {party_size}) joined the waitlist. Estimated wait: ~{est_min} min.",
                role="admin"
            )
            st.success(f"You're #{next_pos} in line! Estimated wait: ~{est_min} minutes.")
            st.rerun()
        else:
            st.error("Name is required.")

    conn.close()
    st.markdown("</div>", unsafe_allow_html=True)


def render_queue_dashboard(user):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT q.*, t.table_number
        FROM queue q
        LEFT JOIN restaurant_tables t ON q.table_id = t.id
        WHERE q.status = 'waiting'
        ORDER BY q.position ASC
    """)
    waiting = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, table_number, capacity, status FROM restaurant_tables WHERE status = 'available' ORDER BY table_number")
    available_tables = [dict(r) for r in cursor.fetchall()]

    cursor.execute("SELECT id, table_number, capacity, status FROM restaurant_tables ORDER BY table_number")
    all_tables = [dict(r) for r in cursor.fetchall()]
    conn.close()

    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:16px;">
            <div style="font-size:0.72rem; color:#71717A; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">In Queue</div>
            <div style="font-size:1.6rem; font-weight:700; color:#C9A86A;">{len(waiting)}</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:16px;">
            <div style="font-size:0.72rem; color:#71717A; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">Available Tables</div>
            <div style="font-size:1.6rem; font-weight:700; color:#22C55E;">{len(available_tables)}</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        occupied = sum(1 for t in all_tables if t["status"] == "occupied")
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:16px;">
            <div style="font-size:0.72rem; color:#71717A; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;">Occupied</div>
            <div style="font-size:1.6rem; font-weight:700; color:#3B82F6;">{occupied}</div>
        </div>
        """, unsafe_allow_html=True)

    if not waiting:
        st.markdown("<p style='color:#71717A; font-size:0.85rem; margin-top:16px;'>No one in the queue.</p>", unsafe_allow_html=True)
        return

    for entry in waiting:
        entry_time = datetime.fromisoformat(entry["created_at"])
        elapsed = int((datetime.now() - entry_time).total_seconds() / 60)
        st.markdown(f"""
        <div class="glass-card" style="padding:16px; margin-bottom:8px; border-left:3px solid #3B82F6;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="width:32px; height:32px; border-radius:50%; background:#1F1F23;
                        display:flex; align-items:center; justify-content:center;
                        border:1px solid rgba(255,255,255,0.06); font-weight:700; color:#C9A86A; font-size:0.85rem;">
                        #{entry['position']}
                    </div>
                    <div>
                        <strong style="color:#FAFAFA;">{entry['customer_name']}</strong>
                        <span style="color:#71717A; font-size:0.8rem;"> &middot; {entry['party_size']} guests &middot; {elapsed}m ago</span>
                    </div>
                </div>
            </div>
            <div style="margin-top:8px; display:flex; gap:8px;">
        """, unsafe_allow_html=True)

        matching_tables = [t for t in available_tables if t["capacity"] >= entry["party_size"]]
        if matching_tables:
            c1, c2 = st.columns([2, 1])
            with c1:
                seat_options = {f"{t['table_number']} (Cap: {t['capacity']})": t["id"] for t in matching_tables}
                seat_label = st.selectbox(
                    "Seat at",
                    list(seat_options.keys()),
                    key=f"seat_table_{entry['id']}",
                    label_visibility="collapsed"
                )
                seat_table_id = seat_options[seat_label]
            with c2:
                if st.button("Seat Guest", key=f"seat_q_{entry['id']}", type="primary", use_container_width=True):
                    conn = get_db_connection()
                    cur = conn.cursor()
                    cur.execute("UPDATE queue SET status = 'seated', table_id = ?, seated_at = ? WHERE id = ?",
                               (seat_table_id, datetime.now().isoformat(), entry["id"]))
                    cur.execute("UPDATE restaurant_tables SET status = 'occupied' WHERE id = ?", (seat_table_id,))
                    conn.commit()
                    conn.close()
                    add_notification("Guest Seated", f"{entry['customer_name']} seated at {seat_label.split(' (')[0]}", role="admin")
                    st.rerun()
        else:
            st.markdown("<p style='color:#71717A; font-size:0.78rem;'>No available tables for this party size.</p>", unsafe_allow_html=True)
            if st.button("Leave Queue", key=f"leave_{entry['id']}", use_container_width=True):
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("UPDATE queue SET status = 'cancelled' WHERE id = ?", (entry["id"],))
                conn.commit()
                conn.close()
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


def render_queue_status(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT q.*, t.table_number
        FROM queue q
        LEFT JOIN restaurant_tables t ON q.table_id = t.id
        WHERE q.customer_name = ? AND q.status = 'waiting'
        ORDER BY q.created_at DESC
    """, (user.get("full_name", ""),))
    entries = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if not entries:
        st.markdown("<p style='color:#71717A; font-size:0.85rem;'>You're not in the queue.</p>", unsafe_allow_html=True)
        return

    for e in entries:
        st.markdown(f"""
        <div class="glass-card" style="padding:14px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#FAFAFA; font-weight:600;">Position #{e['position']}</span>
                <span class="badge badge-blue">{e['party_size']} guests</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
