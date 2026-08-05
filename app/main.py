from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .auth import require_admin_user
from .database import init_db
from .routes import router
from .settings import ALLOWED_ORIGINS, SESSION_SECRET_KEY

app = FastAPI(title="Secure Tenant Control Plane", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

app.include_router(router)

@app.on_event("startup")
def on_startup() -> None:
    init_db()

@app.get("/")
def root() -> dict:
    return {
        "status": "ok",
        "message": "Secure Tenant Control Plane is running.",
        "login": "/login",
        "logout": "/logout",
        "user": "GET /api/v1/user",
    }
