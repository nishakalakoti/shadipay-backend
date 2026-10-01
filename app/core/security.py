from firebase_admin import auth
from fastapi import HTTPException, status


def verify_firebase_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)

        return decoded_token

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token.",
            headers={"WWW-Authenticate": "Bearer"},
        )