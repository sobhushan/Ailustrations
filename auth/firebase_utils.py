# auth/firebase_utils.py
import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore
import os
import base64
from io import BytesIO
from google.cloud import firestore
from PIL import Image # type: ignore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\HP INDIA\Desktop\TA\image_ai_expert\Imagino\firebase\firebase_key.json"

# Initialize Firebase if not initialized already
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase/firebase_key.json")
    firebase_admin.initialize_app(cred)

# Correct initialization of Firestore Client
db = firestore.Client()

def compress_image(image_bytes, quality=30):
    try:
        image = Image.open(BytesIO(image_bytes))
        buffer = BytesIO()
        image.save(buffer, format="JPEG", optimize=True, quality=quality)
        return buffer.getvalue()
    except Exception as e:
        print("Compression failed:", e)
        return image_bytes  # Fallback to original


def save_history(email, history):
    formatted = []

    for entry in history:
        if "prompt" not in entry or "feedback" not in entry or "image_bytes" not in entry:
            continue

        image_bytes = entry["image_bytes"]

        if hasattr(image_bytes, "getvalue"):
            image_bytes = image_bytes.getvalue()
        elif isinstance(image_bytes, memoryview):
            image_bytes = bytes(image_bytes)
        elif not isinstance(image_bytes, bytes):
            continue

        # Compress image
        compressed_bytes = compress_image(image_bytes, quality=30)

        # Base64 encode
        image_base64 = base64.b64encode(compressed_bytes).decode("utf-8")

        formatted_entry = {
            "prompt": entry["prompt"],
            "feedback": entry["feedback"],
            "image_base64": image_base64
        }

        formatted.append(formatted_entry)

    if formatted:
        user_doc = db.collection("users").document(email)
        user_doc.set({"history": formatted})

    print(f"History saved for {email}. Total entries: {len(formatted)}")
    print(f"Formatted history: {formatted}")


def load_history(email):
    # Get the document from Firestore
    user_doc = db.collection("users").document(email).get()

    if user_doc.exists:
        raw_history = user_doc.to_dict().get("history", [])
        decoded_history = []

        for item in raw_history:
            # Make sure both 'prompt' and 'feedback' exist
            if "prompt" not in item or "feedback" not in item:
                continue

            # If the base64 image exists, we decode it. Otherwise, we ignore it
            if "image_base64" in item:
                try:
                    image_bytes = base64.b64decode(item["image_base64"])
                except Exception:
                    image_bytes = None  # If decoding fails, we ignore the image
            else:
                image_bytes = None  # If no image is present, we set it to None

            decoded_history.append({
                "prompt": item["prompt"],
                "feedback": item["feedback"],
                "image_bytes": image_bytes
            })

        return decoded_history

    return []



# def save_history(email, history):
#     formatted = []
    
#     for entry in history:
#         # Ensure valid fields
#         if "prompt" not in entry or "feedback" not in entry or "image_bytes" not in entry:
#             continue
        
#         image_bytes = entry["image_bytes"]

#         # Convert image to bytes if needed
#         if hasattr(image_bytes, "getvalue"):
#             image_bytes = image_bytes.getvalue()
#         elif isinstance(image_bytes, memoryview):
#             image_bytes = bytes(image_bytes)
#         elif not isinstance(image_bytes, bytes):
#             continue  # skip invalid image formats

#         # Base64 encode the image bytes
#         image_base64 = base64.b64encode(image_bytes).decode("utf-8")

#         # Construct the formatted entry
#         formatted_entry = {
#             "prompt": entry["prompt"],
#             "feedback": entry["feedback"],
#             "image_base64": image_base64
#         }
        
#         formatted.append(formatted_entry)

#     # Check if the formatted data is too large
#     if len(formatted) > 0:
#         user_doc = db.collection("users").document(email)
#         user_doc.set({"history": formatted})
#     print(f"History saved for {email}. Total entries: {len(formatted)}")
#     print(f"Formatted history: {formatted}")

# def load_history(email):
#     user_doc = db.collection("users").document(email).get()
#     if user_doc.exists:
#         raw_history = user_doc.to_dict().get("history", [])
#         decoded_history = []

#         for item in raw_history:
#             if "prompt" not in item or "feedback" not in item or "image_base64" not in item:
#                 continue

#             try:
#                 image_bytes = base64.b64decode(item["image_base64"])
#             except Exception:
#                 continue  # skip if decoding fails

#             decoded_history.append({
#                 "prompt": item["prompt"],
#                 "feedback": item["feedback"],
#                 "image_bytes": image_bytes
#             })

#         return decoded_history

#     return []
