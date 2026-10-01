from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_firebase_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    return verify_firebase_token(token)


@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user),
):
    return {
        "uid": current_user.get("uid"),
        "email": current_user.get("email"),
        "name": current_user.get("name"),
        "email_verified": current_user.get(
            "email_verified",
            False,
        ),
    }