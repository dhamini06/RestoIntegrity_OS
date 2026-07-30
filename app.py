import streamlit as st
import os
from database import get_db_connection, init_db, migrate_db, add_notification, get_notifications, unread_notification_count, mark_notification_read
from mock_data import seed_db
from components.ui_helpers import inject_custom_css
from components.customer_view import render_customer_view
from components.kitchen_view import render_kitchen_view
from components.manager_view import render_manager_view
from components.reservations_view import render_reservation_view
from components.queue_view import render_queue_view

st.set_page_config(
    page_title="RestoIntegrity OS",
    page_icon="\u2699\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
migrate_db()
seed_db()
inject_custom_css()

user = {
    "id": 1,
    "email": "admin@resto.com",
    "full_name": "Admin",
    "role": "admin",
    "avatar_url": "",
}

ROLE_MAP = {
    "admin":    ["Manager Dashboard", "Reservations", "Queue", "Customer Menu", "Kitchen View"],
    "staff":    ["Reservations", "Queue", "Customer Menu", "Kitchen View"],
    "kitchen":  ["Kitchen View"],
    "customer": ["Customer Menu", "Reservations", "Queue"],
}

allowed_views = ROLE_MAP.get(user["role"], ["Customer Menu"])

avatar_letter = user.get("full_name", "?")[0].upper()
avatar_url = user.get("avatar_url", "")

if avatar_url:
    avatar_html = f'<img src="{avatar_url}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; margin:0 auto 8px; border:1px solid rgba(201,168,106,0.2);">'
else:
    avatar_html = f'<div style="width:40px; height:40px; border-radius:50%; background:#C9A86A; display:flex; align-items:center; justify-content:center; margin:0 auto 8px; box-shadow:0 4px 16px rgba(201,168,106,0.15);"><span style="color:#09090B; font-weight:700; font-size:0.85rem;">{avatar_letter}</span></div>'

st.sidebar.markdown(f"""
<div style="background: #1F1F23; border-radius: 16px; padding: 16px; margin: 0 0 16px 0;
    border: 1px solid rgba(255,255,255,0.06); text-align:center;">
    {avatar_html}
    <div style="font-size:0.82rem; color:#A1A1AA; letter-spacing:0.01em; font-weight:500;">Welcome back</div>
    <div style="font-size:1rem; font-weight:700; color:#FAFAFA; margin:2px 0 8px;">{user['full_name']}</div>
    <span class="badge badge-gold">{user['role'].upper()}</span>
</div>
""", unsafe_allow_html=True)

role = st.sidebar.radio("Navigate", allowed_views, index=0)

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

notif_count = unread_notification_count(role=user["role"])
notif_label = f"Notifications ({notif_count})" if notif_count else "Notifications"
with st.sidebar.expander(notif_label):
    notifs = get_notifications(role=user["role"], limit=10)
    if not notifs:
        st.markdown("<p style='color:#71717A; font-size:0.78rem; text-align:center;'>No notifications</p>", unsafe_allow_html=True)
    else:
        for n in notifs:
            type_icon = {"info": "i", "success": "\u2713", "warning": "!", "alert": "\u26a0"}.get(n["type"], "i")
            st.markdown(f"""
            <div style="background:{'#1F1F23' if not n['is_read'] else 'transparent'}; border-radius:10px; padding:8px; margin-bottom:4px; font-size:0.78rem; cursor:pointer;">
                <div style="display:flex; justify-content:space-between;">
                    <strong style="color:#FAFAFA;">{n['title']}</strong>
                    <span style="color:#71717A;">{n['created_at'][:10]}</span>
                </div>
                <p style="color:#A1A1AA; margin:2px 0 0; font-size:0.75rem;">{n['message']}</p>
            </div>
            """, unsafe_allow_html=True)
            if not n["is_read"] and st.button("Mark read", key=f"read_{n['id']}", use_container_width=True):
                mark_notification_read(n["id"])
                st.rerun()

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

if user["role"] == "admin":
    st.sidebar.markdown("<div style='font-size:0.75rem; color:#71717A; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;'>AI Settings</div>", unsafe_allow_html=True)
    api_key = st.sidebar.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""), label_visibility="collapsed", placeholder="Gemini API Key")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    else:
        os.environ.pop("GEMINI_API_KEY", None)

st.markdown("""
<div style="background: #18181B; border: 1px solid rgba(255,255,255,0.06);
     border-radius: 20px; padding: 20px 24px; margin-bottom: 24px;
     box-shadow: 0 8px 32px rgba(0,0,0,0.3);
     animation: fadeInUp 0.5s ease-out;">
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:40px; height:40px; border-radius:12px; background:#C9A86A;
            display:flex; align-items:center; justify-content:center;
            box-shadow: 0 4px 16px rgba(201,168,106,0.15);">
            <span style="color:#09090B; font-weight:800; font-size:1.2rem;">R</span>
        </div>
        <div>
            <h1 style="color: #FAFAFA; margin: 0; font-size: 1.4rem; font-weight: 700; letter-spacing: 0.02em;">
                RestoIntegrity OS
            </h1>
            <p style="color: #71717A; margin: 2px 0 0 0; font-size: 0.82rem; font-weight: 400; letter-spacing: 0.01em;">
                AI-Powered Smart Restaurant Operations Platform
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if role == "Manager Dashboard":
    render_manager_view(user)
elif role == "Customer Menu":
    render_customer_view(user)
elif role == "Kitchen View":
    render_kitchen_view(user)
elif role == "Reservations":
    render_reservation_view(user)
elif role == "Queue":
    render_queue_view(user)
