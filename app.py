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

def authenticate(username, password):
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
            (username, hash_password(password))
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
    except Exception as e:
        st.error(f"System initializing... Please refresh and try again.")
    return None

def login_form():
    st.sidebar.markdown("<h3 style='color:#5D4037; font-family:Playfair Display, serif;'>🔐 Sign In</h3>", unsafe_allow_html=True)
    username = st.sidebar.text_input("Username", key="login_user", placeholder="Username")
    password = st.sidebar.text_input("Password", type="password", key="login_pass", placeholder="Password")

    if st.sidebar.button("🚀 Sign In", key="login_btn", type="primary", use_container_width=True):
        user = authenticate(username, password)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials. Try again!")

    if "user" not in st.session_state:
        st.sidebar.markdown("""
        <div style="background: #F8F3E9; border-radius: 12px; padding: 14px; margin-top: 16px; border: 1px solid #E8D5A3;">
            <div style="font-size:0.75rem; color:#8C7A6B; font-weight:600; margin-bottom:6px;">Demo Credentials</div>
            <div style="font-size:0.8rem; color:#5D4037; line-height:1.6;">
                <b>admin</b> / admin123<br>
                <b>alice</b> / alice123<br>
                <b>bob</b> / bob123<br>
                <b>chef_ramsay</b> / chef123
            </div>
        </div>
        """, unsafe_allow_html=True)

def login_form_main():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: white; border-radius: 20px; padding: 40px 36px;
             box-shadow: 0 8px 40px rgba(197, 165, 90, 0.12); border: 1px solid #E8D5A3;
             animation: fadeInUp 0.6s ease-out;">
            <div style="text-align:center; margin-bottom: 24px;">
                <div style="font-size:2.5rem;">📊</div>
                <h2 style="color:#2C1810; margin: 8px 0 4px; font-weight:800; font-family:Playfair Display, serif;">RestoIntegrity OS</h2>
                <p style="color:#8C7A6B; font-size:0.85rem; margin:0; font-family:Inter, sans-serif;">Sign in to your dashboard</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form_main"):
            username = st.text_input("Username", placeholder="Username", key="login_user_main")
            password = st.text_input("Password", type="password", placeholder="Password", key="login_pass_main")
            if st.form_submit_button("🚀 Sign In", type="primary", use_container_width=True):
                user = authenticate(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try again!")

        st.markdown("""
            <div style="margin-top:20px; padding:14px; background:#F8F3E9; border-radius:12px; border:1px solid #E8D5A3;">
                <div style="font-size:0.75rem; color:#8C7A6B; font-weight:600; margin-bottom:8px;">Demo Credentials</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.85rem; color:#5D4037;">
                    <div><b>admin</b> / admin123</div>
                    <div><b>alice</b> / alice123</div>
                    <div><b>bob</b> / bob123</div>
                    <div><b>chef_ramsay</b> / chef123</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def get_current_user():
    return st.session_state.get("user", None)

user = get_current_user()

if not user:
    login_form()
    login_form_main()
    st.stop()

login_form()

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
