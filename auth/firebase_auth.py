# auth/firebase_auth.py
import requests
import os
import json
import base64
import firebase_admin # type: ignore
from firebase_admin import credentials, auth as admin_auth # type: ignore
from dotenv import load_dotenv

load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_KEY_B64 = os.getenv("FIREBASE_KEY_B64")

FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIREBASE_REFRESH_URL = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"
FIREBASE_VERIFY_EMAIL_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"
FIREBASE_RESET_PASSWORD_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_API_KEY}"

FIREBASE_KEY_DICT = json.loads(base64.b64decode(FIREBASE_KEY_B64).decode("utf-8"))

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_DICT) 
    firebase_admin.initialize_app(cred)

def send_verification_email(id_token: str):
    payload = {
        "requestType": "VERIFY_EMAIL",
        "idToken": id_token
    }
    response = requests.post(FIREBASE_VERIFY_EMAIL_URL, data=payload)
    return response 

def signup(email: str, password: str):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(FIREBASE_SIGNUP_URL, data=payload)
    if response.status_code == 200:
        id_token = response.json()["idToken"]
        send_verification_email(id_token)
    
    return response

def login(email: str, password: str):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(FIREBASE_SIGNIN_URL, data=payload)
    if response.status_code == 200:
        data = response.json()
        id_token = data["idToken"]

        # ✅ Check emailVerified via getAccountInfo
        verify_payload = {"idToken": id_token}
        info_res = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}",
            data=verify_payload,
        )

        if info_res.status_code == 200:
            users = info_res.json().get("users", [])
            if users and not users[0].get("emailVerified", False):
                return {"error": "Email not verified. Please check your inbox."}
        else:
            return {"error": "Could not verify email status."}
    return response

# ✅ Token verification using Firebase Admin
def verify_id_token(id_token: str):
    try:
        decoded_token = admin_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"[Token Verification Error] {e}")
        return None

# 🔄 Refresh token using refresh token
def refresh_id_token(refresh_token: str):
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(FIREBASE_REFRESH_URL, data=payload)
    return response.json()

def send_password_reset_email(email: str):
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    response = requests.post(FIREBASE_RESET_PASSWORD_URL, data=payload)
    return response

def check_if_email_exists(email: str):
    payload = {"email": [email]}
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"
    response = requests.post(url, json=payload)
    return response
