import os
import json
import urllib.parse
import urllib.request
from typing import Optional

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def _get_google_credentials():
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID") or os.getenv("google_oauth_client_id", "")
    client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET") or os.getenv("google_oauth_client_secret", "")
    redirect_uri = os.getenv("GOOGLE_OAUTH_REDIRECT_URI") or os.getenv("google_oauth_redirect_uri", "")
    return client_id, client_secret, redirect_uri

def is_google_oauth_configured() -> bool:
    client_id, client_secret, redirect_uri = _get_google_credentials()
    return bool(client_id and client_secret and redirect_uri)

def get_google_auth_url() -> Optional[str]:
    client_id, _, redirect_uri = _get_google_credentials()
    if not client_id or not redirect_uri:
        return None
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

def exchange_google_code(code: str) -> Optional[dict]:
    client_id, client_secret, redirect_uri = _get_google_credentials()
    if not all([client_id, client_secret, redirect_uri]):
        return None
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    req = urllib.request.Request(
        GOOGLE_TOKEN_URL,
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            token_data = json.loads(resp.read().decode())
            return token_data
    except Exception as e:
        print(f"[OAuth] Token exchange failed: {e}")
        return None

def get_google_user_info(access_token: str) -> Optional[dict]:
    req = urllib.request.Request(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            user_info = json.loads(resp.read().decode())
            return {
                "google_id": user_info.get("id"),
                "email": user_info.get("email", "").lower().strip(),
                "full_name": user_info.get("name", ""),
                "avatar_url": user_info.get("picture", ""),
            }
    except Exception as e:
        print(f"[OAuth] User info fetch failed: {e}")
        return None
