from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.api.weddings import router as wedding_router
from app.api.guests import router as guest_router
from app.api.gifts import router as gift_router
from app.api.invitations import router as invitation_router
from app.api.analytics import router as analytics_router
from app.api.activities import router as activities_router
from app.api.payments import router as payment_router
from app.api.reports import router as reports_router
from app.api.qr_codes import router as qr_router
from app.api.wedding_overview import router as wedding_overview_router

from app.core.firebase import firebase_app
from app.core.config import settings
from app.db.database import engine


app = FastAPI(
    title="ShadiPay API",
    version="1.0.0",
)


# =====================================================
# CORS
# =====================================================

allowed_origins = [
    origin.strip()
    for origin in settings.ALLOWED_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# UPLOADS DIRECTORY
# =====================================================

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads",
)


# =====================================================
# DATABASE STARTUP CHECK
# =====================================================

@app.on_event("startup")
def startup():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("DATABASE CONNECTED SUCCESSFULLY")

    except Exception as error:
        print("DATABASE CONNECTION FAILED")
        print(f"Error: {error}")


# =====================================================
# API ROUTERS
# =====================================================

app.include_router(auth_router)
app.include_router(wedding_router)
app.include_router(guest_router)
app.include_router(gift_router)
app.include_router(invitation_router)
app.include_router(analytics_router)
app.include_router(activities_router)
app.include_router(payment_router)
app.include_router(reports_router)
app.include_router(qr_router)
app.include_router(wedding_overview_router)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "ShadiPay Backend is running"
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok"
    }