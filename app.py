import streamlit as st
import os
import hashlib
from database import get_db_connection, init_db, migrate_db
from mock_data import seed_db
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

def login_form():
    st.sidebar.markdown("<h3 class='glow-indigo'>🔐 Sign In</h3>", unsafe_allow_html=True)
    username = st.sidebar.text_input("Username", key="login_user", placeholder="Enter username")
    password = st.sidebar.text_input("Password", type="password", key="login_pass", placeholder="Enter password")

    if st.sidebar.button("🚀 Sign In", key="login_btn", type="primary", use_container_width=True):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, role, full_name FROM users WHERE username = ? AND password_hash = ?",
            (username, hash_password(password))
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            st.session_state.user = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                "full_name": user["full_name"],
            }
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials. Try again!")

    if "user" not in st.session_state:
        st.sidebar.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(236,72,153,0.08));
             border-radius: 12px; padding: 14px; margin-top: 16px; border: 1px solid rgba(99,102,241,0.12);">
            <div style="font-size:0.75rem; color:#64748b; font-weight:600; margin-bottom:6px;">Demo Credentials</div>
            <div style="font-size:0.8rem; color:#1e293b; line-height:1.6;">
                <b>admin</b> / admin123<br>
                <b>alice</b> / alice123<br>
                <b>bob</b> / bob123<br>
                <b>chef_ramsay</b> / chef123
            </div>
        </div>
        """, unsafe_allow_html=True)

def get_current_user():
    return st.session_state.get("user", None)

user = get_current_user()

if not user:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
         padding: 50px 30px; border-radius: 24px; text-align: center;
         margin-top: 60px; box-shadow: 0 20px 60px rgba(99,102,241,0.3);
         animation: fadeInUp 0.8s ease-out;">
        <h1 style="color: white; font-size: 3rem; font-weight: 900; margin: 0; letter-spacing: -0.03em;">
            📊 RestoIntegrity OS
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-top: 10px; font-weight: 400;">
            AI-Powered Smart Restaurant Operations Platform
        </p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 20px;">
            Sign in using the sidebar to access your dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    login_form()
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
<div style="background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(236,72,153,0.08));
     border-radius: 14px; padding: 14px; margin: 12px 0; border: 1px solid rgba(99,102,241,0.12);">
    <div style="font-size:0.8rem; color:#64748b;">Welcome back,</div>
    <div style="font-size:1.1rem; font-weight:700; color:#1e293b;">{user['full_name']}</div>
    <div style="margin-top:4px;"><span class="badge badge-indigo">{user['role'].upper()}</span></div>
</div>
""", unsafe_allow_html=True)

role = st.sidebar.radio("Navigate to:", allowed_views, index=0)

st.sidebar.markdown("---")

if user["role"] == "admin":
    st.sidebar.markdown("<h4 class='glow-amber'>⚙️ AI Settings</h4>", unsafe_allow_html=True)
    api_key = st.sidebar.text_input("Gemini API Key:", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        st.sidebar.success("AI enabled!")
    else:
        os.environ.pop("GEMINI_API_KEY", None)

st.markdown("""
<div style="background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
     padding: 18px 24px; border-radius: 18px; margin-bottom: 25px;
     box-shadow: 0 8px 30px rgba(99,102,241,0.2);
     animation: fadeInUp 0.5s ease-out;">
    <h1 style="color: white; margin: 0; font-size: 1.8rem; font-weight: 800; text-align: center;">
        📊 RestoIntegrity OS
    </h1>
    <p style="color: rgba(255,255,255,0.85); margin: 5px 0 0 0; font-size: 0.9rem; text-align: center; font-weight: 400;">
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
