import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST_KEY = "smtp_host"
SMTP_PORT_KEY = "smtp_port"
SMTP_USER_KEY = "smtp_user"
SMTP_PASS_KEY = "smtp_pass"
SMTP_FROM_KEY = "smtp_from_email"

def _get_smtp_config():
    host = os.getenv("SMTP_HOST") or os.getenv("smtp_host", "")
    port = int(os.getenv("SMTP_PORT") or os.getenv("smtp_port", "587"))
    user = os.getenv("SMTP_USER") or os.getenv("smtp_user", "")
    passwd = os.getenv("SMTP_PASS") or os.getenv("smtp_pass", "")
    from_email = os.getenv("SMTP_FROM_EMAIL") or os.getenv("smtp_from_email", user)
    return host, port, user, passwd, from_email

def is_smtp_configured() -> bool:
    host, port, user, passwd, from_email = _get_smtp_config()
    return bool(host and user and passwd)

def send_otp_email(to_email: str, otp: str, expires_minutes: int = 5) -> bool:
    host, port, user, passwd, from_email = _get_smtp_config()
    if not host or not user or not passwd:
        return False

    subject = "Your RestoIntegrity OS verification code"
    body_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: 'Manrope', -apple-system, sans-serif; background:#09090B; margin:0; padding:0;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#09090B; padding:40px 0;">
            <tr>
                <td align="center">
                    <table width="400" cellpadding="0" cellspacing="0" style="background:#18181B; border-radius:24px; border:1px solid rgba(255,255,255,0.06); padding:40px;">
                        <tr>
                            <td align="center" style="padding-bottom:24px;">
                                <div style="width:48px; height:48px; border-radius:14px; background:#C9A86A; display:inline-flex; align-items:center; justify-content:center; box-shadow:0 8px 24px rgba(201,168,106,0.15);">
                                    <span style="color:#09090B; font-weight:800; font-size:1.4rem;">R</span>
                                </div>
                                <h2 style="color:#FAFAFA; font-size:1.2rem; font-weight:700; margin:16px 0 4px;">RestoIntegrity OS</h2>
                                <p style="color:#71717A; font-size:0.82rem; margin:0;">Your verification code</p>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" style="background:#1A1810; border-radius:14px; border:1px solid rgba(201,168,106,0.15); padding:24px; margin:16px 0;">
                                <p style="color:#C9A86A; font-size:0.72rem; font-weight:600; text-transform:uppercase; letter-spacing:0.06em; margin:0 0 12px;">Verification Code</p>
                                <div style="font-size:2.4rem; font-weight:700; color:#FAFAFA; letter-spacing:0.25em; font-family:monospace;">{otp}</div>
                                <p style="color:#71717A; font-size:0.75rem; margin:16px 0 0;">This code expires in {expires_minutes} minutes.</p>
                            </td>
                        </tr>
                        <tr>
                            <td align="center" style="padding-top:16px;">
                                <p style="color:#52525B; font-size:0.72rem; margin:0;">If you didn't request this code, you can safely ignore this email.</p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.attach(MIMEText(f"Your RestoIntegrity OS verification code is: {otp}\n\nThis code expires in {expires_minutes} minutes.", "plain"))
    msg.attach(MIMEText(body_html, "html"))

    try:
        ctx = ssl.create_default_context()
        with smtplib.SMTP(host, port, timeout=30) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(user, passwd)
            server.sendmail(from_email, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[Email Service] Failed to send email to {to_email}: {e}")
        return False
