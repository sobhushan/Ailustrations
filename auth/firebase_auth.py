# auth/firebase_auth.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
FIREBASE_SIGNIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

def signup(email: str, password: str):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(FIREBASE_SIGNUP_URL, data=payload)

def login(email: str, password: str):
    payload = {"email": email, "password": password, "returnSecureToken": True}
    return requests.post(FIREBASE_SIGNIN_URL, data=payload)
