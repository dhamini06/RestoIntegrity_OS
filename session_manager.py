from datetime import datetime, timedelta
from database import get_db_connection
from security import generate_session_token

SESSION_DURATION_HOURS = 12
INACTIVITY_TIMEOUT_MINUTES = 30

def create_session(user_id: int, ip_address: str = "", device_info: str = "") -> str:
    token = generate_session_token()
    now = datetime.now()
    expires_at = (now + timedelta(hours=SESSION_DURATION_HOURS)).isoformat()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_sessions (user_id, session_token, ip_address, device_info, created_at, last_activity, expires_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, token, ip_address, device_info, now.isoformat(), now.isoformat(), expires_at),
    )
    conn.commit()
    conn.close()
    return token

def validate_session(session_token: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT s.*, u.email, u.full_name, u.role, u.avatar_url FROM user_sessions s JOIN users u ON s.user_id = u.id WHERE s.session_token = ? AND s.is_active = 1",
        (session_token,),
    )
    session = cursor.fetchone()
    conn.close()
    if not session:
        return {}
    session = dict(session)
    now = datetime.now()
    expires_at = datetime.fromisoformat(session["expires_at"])
    last_activity = datetime.fromisoformat(session["last_activity"])
    if now > expires_at:
        deactivate_session(session_token)
        return {}
    if (now - last_activity).total_seconds() > INACTIVITY_TIMEOUT_MINUTES * 60:
        deactivate_session(session_token)
        return {}
    touch_session(session_token)
    return {
        "id": session["user_id"],
        "email": session["email"],
        "full_name": session["full_name"],
        "role": session["role"],
        "avatar_url": session["avatar_url"] or "",
    }

def touch_session(session_token: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_sessions SET last_activity = ? WHERE session_token = ?",
        (datetime.now().isoformat(), session_token),
    )
    conn.commit()
    conn.close()

def deactivate_session(session_token: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_sessions SET is_active = 0 WHERE session_token = ?",
        (session_token,),
    )
    conn.commit()
    conn.close()

def deactivate_all_user_sessions(user_id: int, keep_token: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if keep_token:
        cursor.execute(
            "UPDATE user_sessions SET is_active = 0 WHERE user_id = ? AND session_token != ?",
            (user_id, keep_token),
        )
    else:
        cursor.execute(
            "UPDATE user_sessions SET is_active = 0 WHERE user_id = ?",
            (user_id,),
        )
    conn.commit()
    conn.close()

def cleanup_expired_sessions():
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("UPDATE user_sessions SET is_active = 0 WHERE expires_at < ?", (now,))
    conn.commit()
    conn.close()
