import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tenant_control_plane.db")
PWPUSH_API_BASE_URL = os.getenv("PWPUSH_API_BASE_URL", "https://pwpush.example.com")
PWPUSH_API_TOKEN = os.getenv("PWPUSH_API_TOKEN", "")
TENANT_SECRET_SALT = os.getenv("TENANT_SECRET_SALT", "replace-me")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "replace-me-session-key")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
OIDC_ALLOWED_DOMAIN = os.getenv("OIDC_ALLOWED_DOMAIN", "")
OIDC_REDIRECT_URI = os.getenv("OIDC_REDIRECT_URI", "http://localhost:8000/auth/callback")
OIDC_SCOPES = os.getenv("OIDC_SCOPES", "openid email profile")
