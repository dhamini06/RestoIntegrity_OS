import streamlit as st
import os
import hashlib
import sqlite3
from database import get_db_connection, init_db, migrate_db
from mock_data import seed_db, _hash
from components.ui_helpers import inject_custom_css
from components.customer_view import render_customer_view
from components.kitchen_view import render_kitchen_view
from components.manager_view import render_manager_view

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(email, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM users")
        if cursor.fetchone()["cnt"] == 0:
            conn.close()
            init_db()
            migrate_db()
            seed_db()
            conn = get_db_connection()
            cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, role, full_name FROM users WHERE username = ? AND password_hash = ?",
            (email, hash_password(password))
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            return {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                "full_name": user["full_name"],
            }
    except Exception:
        st.error("System initializing... Please refresh and try again.")
    return None

def lookup_user(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, full_name FROM users WHERE username = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    except Exception:
        return None

def render_login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="background: #18181B; border-radius: 24px; padding: 48px 40px;
             box-shadow: 0 24px 80px rgba(0,0,0,0.5);
             border: 1px solid rgba(255,255,255,0.06);
             animation: fadeInUp 0.6s ease-out; margin-top: 40px;">
            <div style="text-align:center; margin-bottom: 32px;">
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

            if st.button("Sign In", key="google_continue", use_container_width=True):
                st.session_state.login_page = "google_email"
                st.rerun()

        elif page == "google_email":
            st.markdown("""
            <div style="text-align:center; margin-bottom:24px;">
                <div style="width:40px; height:40px; border-radius:10px; background:#1F1F23;
                    display:flex; align-items:center; justify-content:center; margin:0 auto 12px;
                    border:1px solid rgba(255,255,255,0.06);">
                    <span style="color:#A1A1AA; font-weight:600; font-size:0.9rem;">@</span>
                </div>
                <h3 style="color:#FAFAFA; margin:0 0 4px; font-family:Manrope, sans-serif; font-weight:600; font-size:1.1rem;">Sign in</h3>
                <p style="color:#71717A; font-size:0.8rem; margin:0;">Enter your email to continue</p>
            </div>
            """, unsafe_allow_html=True)

            google_email = st.text_input("Email address", placeholder="you@example.com", key="google_email_input", value=st.session_state.get("google_email_val", ""))
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Back", key="google_back", use_container_width=True):
                    st.session_state.login_page = "main"
                    st.session_state.pop("google_email_val", None)
                    st.rerun()
            with col_b2:
                if st.button("Next", key="google_next", type="primary", use_container_width=True):
                    if google_email:
                        user_data = lookup_user(google_email)
                        if user_data:
                            st.session_state.google_email_val = google_email
                            st.session_state.google_user_data = user_data
                            st.session_state.login_page = "google_password"
                            st.rerun()
                        else:
                            st.error("No account found with this email.")

        elif page == "google_password":
            user_data = st.session_state.get("google_user_data", {})
            initials = "".join(p[0] for p in user_data.get("full_name", "?").split()[:2]).upper()

            st.markdown(f"""
            <div style="text-align:center; margin-bottom:24px;">
                <div style="width:48px; height:48px; border-radius:50%; background:#1F1F23;
                    display:flex; align-items:center; justify-content:center; font-size:1rem;
                    font-weight:700; color:#FAFAFA; margin:0 auto 12px;
                    border:1px solid rgba(201,168,106,0.2); letter-spacing:0.02em;">
                    {initials}
                </div>
                <div style="font-weight:600; color:#FAFAFA; font-size:1rem;">{user_data.get('full_name', '')}</div>
                <div style="font-size:0.78rem; color:#71717A;">{user_data.get('username', '')}</div>
            </div>
            """, unsafe_allow_html=True)

            google_pass = st.text_input("Password", type="password", placeholder="Enter your password", key="google_pass_input")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Back", key="google_pass_back", use_container_width=True):
                    st.session_state.login_page = "google_email"
                    st.rerun()
            with col_b2:
                if st.button("Sign In", key="google_signin", type="primary", use_container_width=True):
                    user = authenticate(user_data.get("username", ""), google_pass)
                    if user:
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error("Wrong password. Try again.")

        st.markdown("""
        <div style="text-align:center; margin-top:24px;">
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
    "admin":    ["Manager Dashboard", "Customer Menu", "Kitchen View"],
    "staff":    ["Customer Menu", "Kitchen View"],
    "kitchen":  ["Kitchen View"],
    "customer": ["Customer Menu"],
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
