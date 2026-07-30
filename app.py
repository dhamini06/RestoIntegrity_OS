import streamlit as st
import os
from datetime import datetime
from database import get_db_connection, init_db, migrate_db, add_notification, get_notifications, unread_notification_count, mark_notification_read
from mock_data import seed_db
from components.ui_helpers import inject_custom_css, inject_auth_css
from components.customer_view import render_customer_view
from components.kitchen_view import render_kitchen_view
from components.manager_view import render_manager_view
from components.reservations_view import render_reservation_view
from components.queue_view import render_queue_view
from authentication import (
    request_otp, verify_otp_and_login, login_with_google, logout,
    is_google_oauth_configured, get_google_auth_url, set_login_context,
)
from session_manager import validate_session, deactivate_session

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

set_login_context(device="Streamlit Web App")


def try_restore_session():
    token = st.session_state.get("session_token")
    if token:
        user = validate_session(token)
        if user:
            st.session_state.user = user
            st.session_state.session_token = token
            return True
        else:
            st.session_state.pop("session_token", None)
            st.session_state.pop("user", None)
            st.session_state["session_expired"] = True
            st.rerun()
    return False


def render_login_page():
    inject_auth_css()

    page = st.session_state.get("login_page", "main")

    # ─── Background ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="auth-bg">
        <div class="auth-bg-grid"></div>
        <div class="auth-bg-glow"></div>
        <div class="auth-bg-glow-2"></div>
        <div class="auth-bg-glow-3"></div>
        <div class="auth-bg-circle auth-bg-circle-1"></div>
        <div class="auth-bg-circle auth-bg-circle-2"></div>
        <div class="auth-bg-circle auth-bg-circle-3"></div>
        <div class="auth-bg-ray auth-bg-ray-1"></div>
        <div class="auth-bg-ray auth-bg-ray-2"></div>
        <div class="auth-bg-ray auth-bg-ray-3"></div>
        <div class="auth-particle"></div><div class="auth-particle"></div><div class="auth-particle"></div>
        <div class="auth-particle"></div><div class="auth-particle"></div><div class="auth-particle"></div>
        <div class="auth-particle"></div><div class="auth-particle"></div><div class="auth-particle"></div>
        <div class="auth-particle"></div><div class="auth-particle"></div><div class="auth-particle"></div>
    </div>
    """, unsafe_allow_html=True)

    # ═══════════ CENTERED AUTH PANEL ═══════════════════════════════════════
    _, center_col, _ = st.columns([1, 1, 1])
    with center_col:
        if page == "main":
            st.markdown("""
            <div class="auth-card-logo">
                <div class="auth-card-logo-hex">
                    <div class="auth-card-logo-hex-inner"><span>R</span></div>
                </div>
            </div>
            <div class="auth-card-heading">
                <h2>RestoIntegrity OS</h2>
            </div>
            <p class="auth-card-subtitle">Enter your email to sign in or create an account</p>
            <div class="auth-card-divider"></div>
            """, unsafe_allow_html=True)

            google_configured = is_google_oauth_configured()
            if google_configured:
                google_url = get_google_auth_url()
                if google_url:
                    st.markdown(f"""
                    <a href="{google_url}" target="_self" style="text-decoration:none;">
                        <button class="auth-google-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
                            Continue with Google
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                    st.markdown('<div class="auth-divider-or"><div class="auth-divider-or-line"></div><span class="auth-divider-or-text">or</span><div class="auth-divider-or-line"></div></div>', unsafe_allow_html=True)

            if st.button("Continue with Email", key="auth_email_btn", use_container_width=True):
                st.session_state.login_page = "email"
                st.rerun()

            st.markdown("""
            <div class="auth-security">
                <div class="auth-security-item">
                    <div class="auth-security-icon">&#128274;</div>
                    <div class="auth-security-title">Secure</div>
                    <div class="auth-security-desc">End-to-end Encryption</div>
                </div>
                <div class="auth-security-item">
                    <div class="auth-security-icon">&#10003;</div>
                    <div class="auth-security-title">Verified</div>
                    <div class="auth-security-desc">OTP Protected</div>
                </div>
                <div class="auth-security-item">
                    <div class="auth-security-icon">&#9889;</div>
                    <div class="auth-security-title">Fast</div>
                    <div class="auth-security-desc">Quick Access</div>
                </div>
            </div>
            <div class="auth-card-footer">
                <p>By signing in you agree to our <a href="#">Terms</a> and <a href="#">Privacy Policy</a></p>
            </div>
            <div class="auth-enterprise">
                <span>Enterprise Grade</span>
                <span class="auth-enterprise-sep">&#183;</span>
                <span>Scalable</span>
                <span class="auth-enterprise-sep">&#183;</span>
                <span>Reliable</span>
            </div>
            """, unsafe_allow_html=True)

        elif page == "email":
            st.markdown("""
            <div class="auth-flow-header">
                <div class="icon-wrap" style="background:rgba(201,168,106,0.1);border-radius:14px;">
                    <span style="font-size:1.2rem;color:#C9A86A;">@</span>
                </div>
                <h3>Enter your email</h3>
                <p>We'll send a verification code</p>
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
                        with st.spinner("Sending verification code..."):
                            result = request_otp(email)
                        if result["success"]:
                            st.session_state.auth_email = email
                            st.session_state.auth_otp_request_id = result["otp_request_id"]
                            st.session_state.auth_email_sent_at = datetime.now().isoformat()
                            st.session_state.auth_otp_value = result.get("otp", "")
                            st.session_state.auth_smtp_configured = result.get("smtp_configured", True)
                            st.session_state.login_page = "otp_sent"
                            st.rerun()
                        else:
                            if "cooldown" in result:
                                st.session_state.auth_cooldown = result["cooldown"]
                                st.session_state.login_page = "otp_sent"
                                st.rerun()
                            else:
                                st.error(result.get("error", "Could not send verification code."))
                    else:
                        st.error("Please enter your email.")

        elif page == "otp_sent":
            email = st.session_state.get("auth_email", "")
            cooldown_remaining = st.session_state.pop("auth_cooldown", 0)

            smtp_configured = st.session_state.get("auth_smtp_configured", True)
            otp_value = st.session_state.get("auth_otp_value", "")

            if not smtp_configured and otp_value:
                st.markdown(f"""
                <div class="auth-flow-header">
                    <div class="icon-wrap" style="background:rgba(26,24,16,0.8);border:1px solid rgba(201,168,106,0.15);border-radius:50%;">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#C9A86A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 7L2 7"/>
                        </svg>
                    </div>
                    <h3>Verification Code</h3>
                    <p>Use this code to sign in for <strong style="color:#C9A86A;">{email}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="text-align:center;padding:20px;background:#1A1810;border:1px solid rgba(201,168,106,0.15);border-radius:16px;margin-bottom:16px;">
                    <div style="font-size:2.5rem;font-weight:800;color:#FAFAFA;letter-spacing:0.3em;font-family:monospace;">{otp_value}</div>
                    <p style="color:#71717A;font-size:0.75rem;margin:8px 0 0;">Expires in 5 minutes</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="auth-flow-header">
                    <div class="icon-wrap" style="background:rgba(26,24,16,0.8);border:1px solid rgba(201,168,106,0.15);border-radius:50%;">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#C9A86A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 7L2 7"/>
                        </svg>
                    </div>
                    <h3>Check your email</h3>
                    <p>We sent a verification code to</p>
                    <p style="color:#C9A86A;font-size:0.85rem;font-weight:600;margin:2px 0 0;">{email}</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class="auth-sent-box">
                    <div class="auth-sent-icon">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"/>
                        </svg>
                    </div>
                    <div class="auth-sent-check">&#10003; Code sent successfully</div>
                    <p class="auth-sent-hint">Expires in 5 minutes. Enter it below.</p>
                </div>
                """, unsafe_allow_html=True)

            if cooldown_remaining > 0:
                st.warning(f"Please wait {cooldown_remaining} seconds before requesting a new code.")

            user_otp = st.text_input("Enter verification code", placeholder="000000", key="auth_otp_input", max_chars=6)

            col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
            with col_b1:
                if st.button("Back", key="auth_otp_back", use_container_width=True):
                    st.session_state.login_page = "email"
                    st.rerun()
            with col_b2:
                if st.button("Verify & Sign In", key="auth_otp_verify", type="primary", use_container_width=True, disabled=not user_otp):
                    if user_otp:
                        with st.spinner("Verifying..."):
                            result = verify_otp_and_login(email, user_otp)
                        if result["success"]:
                            st.session_state.user = {
                                "id": result["user"]["id"],
                                "email": result["user"]["email"],
                                "full_name": result["user"]["full_name"],
                                "role": result["user"]["role"],
                                "avatar_url": result["user"].get("avatar_url", ""),
                            }
                            st.session_state.session_token = result["session_token"]
                            st.session_state.pop("auth_email", None)
                            st.session_state.pop("auth_otp_request_id", None)
                            st.session_state.pop("auth_email_sent_at", None)
                            st.rerun()
                        else:
                            err = result.get("error", "Invalid code. Please try again.")
                            if "attempts_remaining" in result:
                                st.error(f"{err} ({result['attempts_remaining']} left)")
                            else:
                                st.error(err)
                    else:
                        st.error("Please enter the verification code.")
            with col_b3:
                if st.button("Resend Code", key="auth_otp_resend", use_container_width=True):
                    with st.spinner("Sending new code..."):
                        result = request_otp(email)
                    if result["success"]:
                        st.success("New code sent!")
                        st.rerun()
                    else:
                        if "cooldown" in result:
                            st.warning(result["error"])
                        else:
                            st.error(result.get("error", "Could not resend code."))


if "user" not in st.session_state:
    try_restore_session()

if st.session_state.pop("session_expired", False):
    st.warning("Your session has expired. Please sign in again.")

user = st.session_state.get("user")

if not user:
    if "login_page" not in st.session_state:
        st.session_state.login_page = "main"
    render_login_page()
    st.stop()

if st.sidebar.button("Sign Out", key="logout_btn", use_container_width=True):
    token = st.session_state.get("session_token")
    if token:
        logout(token)
    st.session_state.pop("user", None)
    st.session_state.pop("session_token", None)
    st.rerun()

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
