import firebase_admin
from firebase_admin import credentials, firestore, auth
import json
from config import (
    FIREBASE_PROJECT_ID,
    FIREBASE_PRIVATE_KEY_ID,
    FIREBASE_PRIVATE_KEY,
    FIREBASE_CLIENT_EMAIL,
    FIREBASE_CLIENT_ID,
    FIREBASE_AUTH_URI,
    FIREBASE_TOKEN_URI
)

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        # Create credentials dictionary
        cred_dict = {
            "type": "service_account",
            "project_id": FIREBASE_PROJECT_ID,
            "private_key_id": FIREBASE_PRIVATE_KEY_ID,
            "private_key": FIREBASE_PRIVATE_KEY.replace('\\n', '\n') if FIREBASE_PRIVATE_KEY else None,
            "client_email": FIREBASE_CLIENT_EMAIL,
            "client_id": FIREBASE_CLIENT_ID,
            "auth_uri": FIREBASE_AUTH_URI,
            "token_uri": FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{FIREBASE_CLIENT_EMAIL}"
        }
        
        # Create credentials object
        cred = credentials.Certificate(cred_dict)
        
        # Initialize Firebase Admin
        firebase_admin.initialize_app(cred)
    
    # Create Firestore client
    return firestore.client()

# Initialize Firestore
db = initialize_firebase()
