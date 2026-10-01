from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.database import SessionLocal
from app.schemas.wedding import (
    WeddingCreate,
    WeddingResponse,
    WeddingUpdate,
)
from app.services.wedding_service import (
    create_wedding,
    get_weddings,
    get_wedding_by_id,
    update_wedding,
    delete_wedding,
)


router = APIRouter(
    prefix="/api/weddings",
    tags=["Weddings"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# CREATE WEDDING
# POST /api/weddings
# ---------------------------------------------------------

@router.post(
    "",
    response_model=WeddingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_wedding_api(
    wedding_data: WeddingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    firebase_uid = current_user.get("uid")

    return create_wedding(
        db,
        wedding_data,
        firebase_uid,
    )


# ---------------------------------------------------------
# GET ALL WEDDINGS OF CURRENT USER
# GET /api/weddings
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[WeddingResponse],
)
def get_weddings_api(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    firebase_uid = current_user.get("uid")

    return get_weddings(
        db,
        firebase_uid,
    )


# ---------------------------------------------------------
# GET SINGLE WEDDING
# GET /api/weddings/{wedding_id}
# ---------------------------------------------------------

@router.get(
    "/{wedding_id}",
    response_model=WeddingResponse,
)
def get_wedding_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    firebase_uid = current_user.get("uid")

    wedding = get_wedding_by_id(
        db,
        wedding_id,
        firebase_uid,
    )

    if wedding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wedding not found",
        )

    return wedding


# ---------------------------------------------------------
# UPDATE WEDDING
# PATCH /api/weddings/{wedding_id}
# ---------------------------------------------------------

@router.patch(
    "/{wedding_id}",
    response_model=WeddingResponse,
)
def update_wedding_api(
    wedding_id: int,
    wedding_data: WeddingUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    firebase_uid = current_user.get("uid")

    wedding = update_wedding(
        db,
        wedding_id,
        wedding_data,
        firebase_uid,
    )

    if wedding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wedding not found",
        )

    return wedding


# ---------------------------------------------------------
# DELETE WEDDING
# DELETE /api/weddings/{wedding_id}
# ---------------------------------------------------------

@router.delete(
    "/{wedding_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_wedding_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    firebase_uid = current_user.get("uid")

    deleted = delete_wedding(
        db,
        wedding_id,
        firebase_uid,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wedding not found",
        )

    return None