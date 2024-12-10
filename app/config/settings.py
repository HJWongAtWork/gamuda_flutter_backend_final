import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOSTPORT = os.getenv("DB_HOSTPORT")
DB_DBNAME = os.getenv("DB_DBNAME")
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTPORT}/{DB_DBNAME}"

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# CORS Settings
ALLOWED_ORIGINS = [
    "https://gamuda-flutter-homework-01.web.app",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

ALLOWED_METHODS = ["GET", "POST", "OPTIONS"]
ALLOWED_HEADERS = [
    "Content-Type",
    "Accept",
    "Authorization",
    "Origin",
    "X-Requested-With",
    "X-CSRF-Token",
]
