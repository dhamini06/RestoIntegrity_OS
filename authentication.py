from datetime import datetime
from database import get_db_connection
from security import (
    hash_password, verify_password, generate_otp, hash_otp, verify_otp,
    get_otp_expiry, is_expired, sanitize_email, generate_session_token,
)
from email_service import send_otp_email, is_smtp_configured
from session_manager import create_session, deactivate_session
from oauth import (
    is_google_oauth_configured, get_google_auth_url,
    exchange_google_code, get_google_user_info,
)

OTP_EXPIRY_MINUTES = 5
OTP_MAX_ATTEMPTS = 5
OTP_RESEND_COOLDOWN_SECONDS = 30

LOGIN_IP = ""
LOGIN_DEVICE = ""

def set_login_context(ip: str = "", device: str = ""):
    global LOGIN_IP, LOGIN_DEVICE
    LOGIN_IP = ip
    LOGIN_DEVICE = device

def _audit_log(email: str, event_type: str, status: str, user_id: int = None, details: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO login_history (user_id, email, event_type, status, ip_address, device_info, details, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user_id, email, event_type, status, LOGIN_IP, LOGIN_DEVICE, details, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()

def get_or_create_user(email: str, full_name: str, role: str = "staff", avatar_url: str = "", google_id: str = "") -> dict:
    email = sanitize_email(email)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user:
        user = dict(user)
        update_fields = []
        if google_id and not user.get("google_id"):
            update_fields.append(("google_id", google_id))
        if avatar_url and not user.get("avatar_url"):
            update_fields.append(("avatar_url", avatar_url))
        if update_fields:
            set_clause = ", ".join(f"{col} = ?" for col, _ in update_fields)
            values = [val for _, val in update_fields]
            values.append(email)
            cursor.execute(f"UPDATE users SET {set_clause} WHERE email = ?", values)
            conn.commit()
        conn.close()
        return user
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO users (email, password_hash, full_name, role, avatar_url, google_id, email_verified, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (email, None, full_name, role, avatar_url, google_id, 1 if google_id else 0, now, now),
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {
        "id": user_id,
        "email": email,
        "full_name": full_name,
        "role": role,
        "avatar_url": avatar_url,
        "google_id": google_id,
    }

def login_with_password(email: str, password: str) -> dict:
    email = sanitize_email(email)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        _audit_log(email, "login", "failed", details="No account found")
        return {"success": False, "error": "No account found with this email."}
    user = dict(user)
    if not user.get("password_hash"):
        _audit_log(email, "login", "failed", user.get("id"), "Password login not enabled for this account")
        return {"success": False, "error": "This account uses Google sign-in. Please use Continue with Google."}
    if not verify_password(password, user["password_hash"]):
        _audit_log(email, "login", "failed", user["id"], "Invalid password")
        return {"success": False, "error": "Invalid password."}
    token = create_session(user["id"], LOGIN_IP, LOGIN_DEVICE)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now().isoformat(), user["id"]))
    conn.commit()
    conn.close()
    _audit_log(email, "login", "success", user["id"], "Password login")
    return {"success": True, "user": user, "session_token": token}

def request_otp(email: str) -> dict:
    email = sanitize_email(email)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        _audit_log(email, "otp_requested", "failed", details="No account found")
        return {"success": False, "error": "No account found with this email."}
    user = dict(user)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT created_at FROM otp_requests WHERE email = ? ORDER BY id DESC LIMIT 1",
        (email,),
    )
    last = cursor.fetchone()
    if last:
        last_time = datetime.fromisoformat(last["created_at"])
        elapsed = (datetime.now() - last_time).total_seconds()
        if elapsed < OTP_RESEND_COOLDOWN_SECONDS:
            conn.close()
            remaining = int(OTP_RESEND_COOLDOWN_SECONDS - elapsed)
            return {"success": False, "error": f"Please wait {remaining} seconds before requesting a new code.", "cooldown": remaining}
    otp = generate_otp()
    otp_hash = hash_otp(otp)
    expires_at = get_otp_expiry(OTP_EXPIRY_MINUTES)
    cursor.execute(
        "INSERT INTO otp_requests (email, otp_hash, purpose, attempts_remaining, expires_at, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (email, otp_hash, "login", OTP_MAX_ATTEMPTS, expires_at, datetime.now().isoformat()),
    )
    conn.commit()
    otp_request_id = cursor.lastrowid
    conn.close()
    smtp_ok = send_otp_email(email, otp, OTP_EXPIRY_MINUTES)
    if not smtp_ok:
        _audit_log(email, "otp_generated", "warning", user["id"], "SMTP not configured - OTP would be sent via email")
    _audit_log(email, "otp_generated", "success", user["id"], f"OTP request #{otp_request_id}")
    return {"success": True, "otp_request_id": otp_request_id}

def verify_otp_and_login(email: str, otp: str) -> dict:
    email = sanitize_email(email)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM otp_requests WHERE email = ? AND purpose = 'login' AND verified_at IS NULL ORDER BY id DESC LIMIT 1",
        (email,),
    )
    otp_req = cursor.fetchone()
    if not otp_req:
        conn.close()
        _audit_log(email, "otp_verified", "failed", details="No active OTP request found")
        return {"success": False, "error": "No verification code was requested."}
    otp_req = dict(otp_req)
    if is_expired(otp_req["expires_at"]):
        conn.close()
        _audit_log(email, "otp_verified", "failed", details="OTP expired")
        return {"success": False, "error": "This code has expired. Request a new one."}
    if otp_req["attempts_remaining"] <= 0:
        conn.close()
        _audit_log(email, "otp_verified", "failed", details="No attempts remaining")
        return {"success": False, "error": "Too many failed attempts. Request a new code."}
    if not verify_otp(otp, otp_req["otp_hash"]):
        cursor.execute(
            "UPDATE otp_requests SET attempts_remaining = attempts_remaining - 1 WHERE id = ?",
            (otp_req["id"],),
        )
        conn.commit()
        remaining = otp_req["attempts_remaining"] - 1
        conn.close()
        _audit_log(email, "otp_verified", "failed", details=f"Invalid OTP, {remaining} attempts remaining")
        if remaining <= 0:
            return {"success": False, "error": "No attempts remaining. Request a new code."}
        return {"success": False, "error": f"Invalid code. {remaining} attempt(s) remaining.", "attempts_remaining": remaining}
    cursor.execute(
        "UPDATE otp_requests SET verified_at = ? WHERE id = ?",
        (datetime.now().isoformat(), otp_req["id"]),
    )
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = dict(cursor.fetchone())
    if not user.get("email_verified"):
        cursor.execute("UPDATE users SET email_verified = 1 WHERE email = ?", (email,))
    conn.commit()
    token = create_session(user["id"], LOGIN_IP, LOGIN_DEVICE)
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now().isoformat(), user["id"]))
    conn.commit()
    conn.close()
    _audit_log(email, "otp_verified", "success", user["id"], "OTP login successful")
    _audit_log(email, "login", "success", user["id"], "OTP login")
    return {"success": True, "user": user, "session_token": token}

def login_with_google(auth_code: str) -> dict:
    token_data = exchange_google_code(auth_code)
    if not token_data or "access_token" not in token_data:
        _audit_log("unknown", "google_login", "failed", details="Token exchange failed")
        return {"success": False, "error": "Google authentication failed. Please try again."}
    google_user = get_google_user_info(token_data["access_token"])
    if not google_user:
        _audit_log("unknown", "google_login", "failed", details="Failed to fetch user info")
        return {"success": False, "error": "Could not retrieve your profile from Google."}
    user = get_or_create_user(
        email=google_user["email"],
        full_name=google_user["full_name"],
        role="staff",
        avatar_url=google_user["avatar_url"],
        google_id=google_user["google_id"],
    )
    token = create_session(user["id"], LOGIN_IP, LOGIN_DEVICE)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_login = ?, email_verified = 1 WHERE id = ?",
                   (datetime.now().isoformat(), user["id"]))
    conn.commit()
    conn.close()
    _audit_log(user["email"], "google_login", "success", user["id"], "Google OAuth login")
    _audit_log(user["email"], "login", "success", user["id"], "Google login")
    return {"success": True, "user": user, "session_token": token}

def logout(session_token: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, email FROM user_sessions WHERE session_token = ?",
        (session_token,),
    )
    session = cursor.fetchone()
    conn.close()
    if session:
        _audit_log(session["email"], "logout", "success", session["user_id"], "User logged out")
    deactivate_session(session_token)
