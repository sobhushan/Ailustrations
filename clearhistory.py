import firebase_admin
from firebase_admin import credentials, firestore
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\HP INDIA\Desktop\TA\image_ai_expert\Imagino\firebase\firebase_key.json"

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase/firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.Client()

def clear_user_history(email):
    user_doc_ref = db.collection("users").document(email)
    user_doc_ref.update({"history": []})
    print(f"History cleared for {email}")

# Replace with your test email
clear_user_history("sbhushan_be21@thapar.edu")
