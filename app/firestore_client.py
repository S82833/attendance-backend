import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import json
import os
from google.cloud.firestore_v1 import GeoPoint
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    # Estás en local
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    cred = credentials.Certificate(cred_path)
else:
    # Estás en Render: usa JSON desde variable
    firebase_credentials = os.getenv("FIREBASE_APPLICATION_CREDENTIALS")
    cred_dict = json.loads(firebase_credentials)
    cred = credentials.Certificate(cred_dict)

initialize_app(cred)

db = firestore.client()

def save_attendance(uid: str, image_url: str, timestamp: datetime, location: dict, entradaSalida: str):
    try:
        attendance_data = {
            "user_id": uid,
            "timestamp": timestamp,
            "photo_url": image_url,
            "location": GeoPoint(location["lat"], location["lng"]),
            "entradaSalida": entradaSalida
        }
        db.collection("attendances").add(attendance_data)
    except Exception as e:
        print("Error guardando en Firestore:", e)
        raise

def get_all_attendances():
    docs = db.collection("attendances").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    results = []

    for doc in docs:
        data = doc.to_dict()
        results.append({
            "id": doc.id,
            "user_id": data.get("user_id"),
            "timestamp": data.get("timestamp").isoformat() if data.get("timestamp") else None,
            "photo_url": data.get("photo_url"),
            "location": {
                "lat": data["location"].latitude if data.get("location") else None,
                "lng": data["location"].longitude if data.get("location") else None
            },
            "entradaSalida": data.get("entradaSalida")
        })

    return results
