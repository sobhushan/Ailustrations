# auth/firebase_auth.py
import requests
import os
import firebase_admin # type: ignore
from firebase_admin import credentials, auth as admin_auth # type: ignore
from dotenv import load_dotenv
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\Users\HP INDIA\Desktop\TA\image_ai_expert\Imagino\firebase\firebase_key.json"

load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIREBASE_REFRESH_URL = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"

if not firebase_admin._apps:
    # cred = credentials.Certificate("firebase/firebase-adminsdk.json")
    cred = credentials.Certificate("firebase/firebase_key.json")  # adjust path as needed
    firebase_admin.initialize_app(cred)

def signup(email: str, password: str):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(FIREBASE_SIGNUP_URL, data=payload)

def login(email: str, password: str):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(FIREBASE_SIGNIN_URL, data=payload)

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