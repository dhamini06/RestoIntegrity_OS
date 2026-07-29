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
    page_icon="📊",
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
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 24px; padding: 48px 40px;
             box-shadow: 0 12px 60px rgba(197, 165, 90, 0.12);
             border: 1px solid #E8D5A3;
             animation: fadeInUp 0.6s ease-out; margin-top: 30px;">
            <div style="text-align:center; margin-bottom: 32px;">
                <div style="font-size:2.2rem; margin-bottom:4px;">📊</div>
                <h2 style="color:#2C1810; margin: 0 0 4px; font-weight:800;
                    font-family:Playfair Display, serif; font-size:1.6rem;">RestoIntegrity OS</h2>
                <p style="color:#8C7A6B; font-size:0.85rem; margin:0; font-family:Inter, sans-serif;">
                    AI-Powered Restaurant Operations
                </p>
            </div>
        """, unsafe_allow_html=True)

        page = st.session_state.get("login_page", "main")

        if page == "main":
            st.markdown("""
            <div style="text-align:center; margin-bottom:24px;">
                <p style="color:#8C7A6B; font-size:0.85rem; margin:0; font-family:Inter, sans-serif;">
                    Sign in to continue to your dashboard
                </p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Sign in with Google", key="google_continue", use_container_width=True):
                st.session_state.login_page = "google_email"
                st.rerun()

        elif page == "google_email":
            st.markdown("""
            <div style="text-align:center; margin-bottom:20px;">
                <svg width="32" height="32" viewBox="0 0 48 48"><path fill="#4285F4" d="M45.12 24.5c0-1.56-.14-3.06-.4-4.5H24v8.51h11.84c-.51 2.75-2.06 5.08-4.39 6.64v5.52h7.11c4.16-3.83 6.56-9.47 6.56-16.17z"/><path fill="#34A853" d="M24 46c5.94 0 10.92-1.97 14.56-5.33l-7.11-5.52c-1.97 1.32-4.49 2.1-7.45 2.1-5.73 0-10.58-3.87-12.32-9.07H4.34v5.7C7.96 41.07 15.4 46 24 46z"/><path fill="#FBBC05" d="M11.68 28.18C11.18 26.68 10.9 25.08 10.9 23.5s.28-3.18.78-4.68v-5.7H4.34C2.58 16.15 1.5 19.7 1.5 23.5s1.08 7.35 2.84 10.18l7.34-5.5z"/><path fill="#EA4335" d="M24 10.25c3.23 0 6.13 1.11 8.41 3.29l6.31-6.31C34.91 3.87 29.93 2 24 2 15.4 2 7.96 6.93 4.34 13.32l7.34 5.5C13.42 14.12 18.27 10.25 24 10.25z"/></svg>
                <h3 style="color:#2C1810; margin:8px 0 4px; font-family:Playfair Display, serif;">Sign in with Google</h3>
                <p style="color:#8C7A6B; font-size:0.8rem; margin:0;">Use your Google account to sign in</p>
            </div>
            """, unsafe_allow_html=True)

            google_email = st.text_input("Email address", placeholder="you@gmail.com", key="google_email_input", value=st.session_state.get("google_email_val", ""))
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
                <div style="width:64px; height:64px; border-radius:50%; background:#4285F4;
                    display:flex; align-items:center; justify-content:center; font-size:1.4rem;
                    font-weight:500; color:white; margin:0 auto 12px; font-family:Inter;">
                    {initials}
                </div>
                <div style="font-weight:600; color:#2C1810; font-size:1rem;">{user_data.get('full_name', '')}</div>
                <div style="font-size:0.8rem; color:#8C7A6B;">{user_data.get('username', '')}</div>
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
            <p style="font-size:0.75rem; color:#8C7A6B; margin:0;">
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

if "user" in st.session_state and st.sidebar.button("🚪 Sign Out", key="logout_btn", use_container_width=True):
    st.session_state.pop("user", None)
    st.rerun()

ROLE_MAP = {
    "admin":    ["📊 Manager Dashboard", "📱 Customer Menu", "👨‍🍳 Kitchen View"],
    "staff":    ["📱 Customer Menu", "👨‍🍳 Kitchen View"],
    "kitchen":  ["👨‍🍳 Kitchen View"],
    "customer": ["📱 Customer Menu"],
}

allowed_views = ROLE_MAP.get(user["role"], ["📱 Customer Menu"])

st.sidebar.markdown(f"""
<div style="background: #F8F3E9; border-radius: 14px; padding: 14px; margin: 12px 0; border: 1px solid #E8D5A3;">
    <div style="font-size:0.8rem; color:#8C7A6B;">Welcome back,</div>
    <div style="font-size:1.1rem; font-weight:700; color:#2C1810; font-family:Playfair Display, serif;">{user['full_name']}</div>
    <div style="margin-top:4px;"><span class="badge badge-gold">{user['role'].upper()}</span></div>
</div>
""", unsafe_allow_html=True)

role = st.sidebar.radio("Navigate to:", allowed_views, index=0)

st.sidebar.markdown("---")

if user["role"] == "admin":
    st.sidebar.markdown("<h4 style='color:#B8860B; font-family:Playfair Display, serif;'>⚙️ AI Settings</h4>", unsafe_allow_html=True)
    api_key = st.sidebar.text_input("Gemini API Key:", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.sidebar.success("AI enabled!")
    else:
        os.environ.pop("GEMINI_API_KEY", None)

st.markdown("""
<div style="background: linear-gradient(135deg, #C5A55A, #A68332, #8B6914);
     padding: 18px 24px; border-radius: 18px; margin-bottom: 25px;
     box-shadow: 0 8px 30px rgba(197, 165, 90, 0.2);
     animation: fadeInUp 0.5s ease-out;">
    <h1 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 800; text-align: center; font-family: Playfair Display, serif;">
        📊 RestoIntegrity OS
    </h1>
    <p style="color: rgba(255,255,255,0.85); margin: 5px 0 0 0; font-size: 0.9rem; text-align: center; font-weight: 400; font-family: Inter, sans-serif;">
        AI-Powered Smart Restaurant Operations Platform
    </p>
</div>
""", unsafe_allow_html=True)

if role.startswith("📊"):
    render_manager_view(user)
elif role.startswith("📱"):
    render_customer_view(user)
elif role.startswith("👨‍🍳"):
    render_kitchen_view(user)
