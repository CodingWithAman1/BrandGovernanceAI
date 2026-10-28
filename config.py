import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'brandguard-ai-secret-key-2026-synapse')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'brandguard.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif', 'pdf', 'txt', 'md', 'docx'}

    # Firebase Client SDK Configuration (BrandBuild AI Production Keys)
    FIREBASE_CONFIG = {
        "apiKey": os.environ.get("FIREBASE_API_KEY", "AIzaSyDEzSmkRfXfFdlgnghz6QtuuoAwPsLYu3g"),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", "brandbuildai-2749e.firebaseapp.com"),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID", "brandbuildai-2749e"),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", "brandbuildai-2749e.firebasestorage.app"),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", "1063131223920"),
        "appId": os.environ.get("FIREBASE_APP_ID", "1:1063131223920:web:bc9ae6675e2a62f8c4e1b5"),
        "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID", "G-PZ59QGRJPH")
    }
