import streamlit as st
import os
import random
import hashlib
import sqlite3
from database import get_db_connection, init_db, migrate_db
from mock_data import seed_db, _hash
from components.ui_helpers import inject_custom_css
from components.customer_view import render_customer_view
from components.kitchen_view import render_kitchen_view
from components.manager_view import render_manager_view
from components.reservations_view import render_reservation_view
from components.queue_view import render_queue_view
from database import add_notification, get_notifications, unread_notification_count, mark_notification_read

st.set_page_config(
    page_title="RestoIntegrity OS",
    page_icon="\u2699\ufe0f",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
migrate_db()
seed_db()
inject_custom_css()

def lookup_user(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, full_name, role FROM users WHERE username = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    except Exception:
        return None

def sign_in_user(email):
    user_data = lookup_user(email)
    if user_data:
        st.session_state.user = {
            "id": 0,
            "username": user_data["username"],
            "role": user_data["role"],
            "full_name": user_data["full_name"],
        }
        return True
    return False

def generate_otp():
    return str(random.randint(100000, 999999))

def render_login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="background: #18181B; border-radius: 24px; padding: 48px 40px;
             box-shadow: 0 24px 80px rgba(0,0,0,0.5);
             border: 1px solid rgba(255,255,255,0.06);
             animation: fadeInUp 0.6s ease-out; margin-top: 40px;">
            <div style="text-align:center; margin-bottom: 28px;">
                <div style="width:48px; height:48px; border-radius:14px; background:#C9A86A;
                    display:flex; align-items:center; justify-content:center; margin:0 auto 16px;
                    box-shadow: 0 8px 24px rgba(201,168,106,0.15);">
                    <span style="color:#09090B; font-weight:800; font-size:1.4rem;">R</span>
                </div>
                <h2 style="color:#FAFAFA; margin: 0 0 4px; font-weight:700;
                    font-family:Manrope, sans-serif; font-size:1.5rem; letter-spacing:0.02em;">RestoIntegrity OS</h2>
                <p style="color:#71717A; font-size:0.82rem; margin:0; font-weight:400; letter-spacing:0.02em;">
                    AI-Powered Restaurant Operations
                </p>
            </div>
        """, unsafe_allow_html=True)

        page = st.session_state.get("login_page", "main")

        if page == "main":
            st.markdown("""
            <div style="text-align:center; margin-bottom:24px;">
                <p style="color:#A1A1AA; font-size:0.85rem; margin:0;">
                    Sign in to access your dashboard
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Continue with Email", key="auth_email_btn", use_container_width=True):
                st.session_state.login_page = "email"
                st.rerun()

            st.markdown("""
            <div style="text-align:center; margin-top:12px;">
                <p style="color:#52525B; font-size:0.72rem; margin:0;">
                    Secured with OTP verification
                </p>
            </div>
            """, unsafe_allow_html=True)

        elif page == "email":
            st.markdown("""
            <div style="text-align:center; margin-bottom:24px;">
                <div style="width:40px; height:40px; border-radius:10px; background:#1F1F23;
                    display:flex; align-items:center; justify-content:center; margin:0 auto 12px;
                    border:1px solid rgba(255,255,255,0.06);">
                    <span style="color:#A1A1AA; font-weight:600; font-size:0.9rem;">@</span>
                </div>
                <h3 style="color:#FAFAFA; margin:0 0 4px; font-family:Manrope, sans-serif; font-weight:600; font-size:1.05rem;">Enter your email</h3>
                <p style="color:#71717A; font-size:0.8rem; margin:0;">We'll send a verification code</p>
            </div>
            """, unsafe_allow_html=True)

            email = st.text_input("Email address", placeholder="you@example.com", key="auth_email_input", value=st.session_state.get("auth_email", ""))
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Back", key="auth_email_back", use_container_width=True):
                    st.session_state.login_page = "main"
                    st.session_state.auth_email = ""
                    st.rerun()
            with col_b2:
                if st.button("Send Code", key="auth_email_next", type="primary", use_container_width=True):
                    if email:
                        if lookup_user(email):
                            st.session_state.auth_email = email
                            st.session_state.auth_otp = generate_otp()
                            st.session_state.login_page = "otp"
                            st.rerun()
                        else:
                            st.error("No account found with this email.")
                    else:
                        st.error("Please enter your email.")

        elif page == "otp":
            email = st.session_state.get("auth_email", "")
            otp = st.session_state.get("auth_otp", "")
            user_data = lookup_user(email)
            initials = "".join(p[0] for p in user_data.get("full_name", "?").split()[:2]).upper() if user_data else "?"

            st.markdown(f"""
            <div style="text-align:center; margin-bottom:20px;">
                <div style="width:48px; height:48px; border-radius:50%; background:#1F1F23;
                    display:flex; align-items:center; justify-content:center; font-size:1rem;
                    font-weight:700; color:#FAFAFA; margin:0 auto 8px;
                    border:1px solid rgba(201,168,106,0.2); letter-spacing:0.02em;">
                    {initials}
                </div>
                <div style="font-weight:600; color:#FAFAFA; font-size:0.95rem;">{user_data.get('full_name', '') if user_data else ''}</div>
                <div style="font-size:0.78rem; color:#71717A;">{email}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background: #1A1810; border: 1px solid rgba(201,168,106,0.15); border-radius: 14px; padding: 16px; margin-bottom: 20px; text-align:center;">
                <div style="font-size:0.72rem; color:#C9A86A; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:4px;">Verification Code</div>
                <div style="font-size:2rem; font-weight:700; color:#FAFAFA; letter-spacing:0.3em; font-family:monospace;">{otp}</div>
                <p style="font-size:0.72rem; color:#71717A; margin:6px 0 0;">A verification code has been sent to {email}</p>
            </div>
            """, unsafe_allow_html=True)

            user_otp = st.text_input("Enter verification code", placeholder="000000", key="auth_otp_input", max_chars=6)

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Back", key="auth_otp_back", use_container_width=True):
                    st.session_state.login_page = "email"
                    st.rerun()
            with col_b2:
                if st.button("Verify & Sign In", key="auth_otp_verify", type="primary", use_container_width=True):
                    if user_otp == otp:
                        if sign_in_user(email):
                            st.session_state.pop("auth_otp", None)
                            st.session_state.pop("auth_email", None)
                            st.rerun()
                        else:
                            st.error("Could not sign in. Please try again.")
                    else:
                        st.error("Invalid code. Please try again.")

            if st.button("Resend code", key="auth_otp_resend", use_container_width=True):
                st.session_state.auth_otp = generate_otp()
                st.rerun()

        st.markdown("""
        <div style="text-align:center; margin-top:20px;">
            <p style="font-size:0.72rem; color:#52525B; margin:0; letter-spacing:0.01em;">
                By signing in, you agree to our Terms and Privacy Policy.
            </p>
        </div>
        </div>
        """, unsafe_allow_html=True)

def get_current_user():
    return st.session_state.get("user", None)

user = get_current_user()

if not user:
    if "login_page" not in st.session_state:
        st.session_state.login_page = "main"
    render_login_page()
    st.stop()

if "user" in st.session_state and st.sidebar.button("Sign Out", key="logout_btn", use_container_width=True):
    st.session_state.pop("user", None)
    st.rerun()

ROLE_MAP = {
    "admin":    ["Manager Dashboard", "Reservations", "Queue", "Customer Menu", "Kitchen View"],
    "staff":    ["Reservations", "Queue", "Customer Menu", "Kitchen View"],
    "kitchen":  ["Kitchen View"],
    "customer": ["Customer Menu", "Reservations", "Queue"],
}

allowed_views = ROLE_MAP.get(user["role"], ["Customer Menu"])

st.sidebar.markdown(f"""
<div style="background: #1F1F23; border-radius: 16px; padding: 16px; margin: 0 0 16px 0;
    border: 1px solid rgba(255,255,255,0.06); text-align:center;">
    <div style="width:40px; height:40px; border-radius:50%; background:#C9A86A;
        display:flex; align-items:center; justify-content:center; margin:0 auto 8px;
        box-shadow: 0 4px 16px rgba(201,168,106,0.15);">
        <span style="color:#09090B; font-weight:700; font-size:0.85rem;">{user['full_name'][0]}</span>
    </div>
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
