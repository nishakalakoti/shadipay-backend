from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db
from app.services.wedding_service import get_wedding_by_id
from app.schemas.gift import (
    GiftCreate,
    GiftResponse,
    GiftUpdate,
)
from app.services.gift_service import (
    create_gift,
    get_gifts,
    get_gift_by_id,
    update_gift,
    delete_gift,
)


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/gifts",
    tags=["Gifts"],
)


def verify_wedding_access(
    wedding_id: int,
    db: Session,
    current_user: dict,
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
# CREATE GIFT
# POST /api/weddings/{wedding_id}/gifts
# ---------------------------------------------------------

@router.post(
    "",
    response_model=GiftResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_gift_api(
    wedding_id: int,
    gift_data: GiftCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return create_gift(
        db,
        wedding_id,
        gift_data,
    )


# ---------------------------------------------------------
# GET ALL GIFTS
# GET /api/weddings/{wedding_id}/gifts
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[GiftResponse],
)
def get_gifts_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return get_gifts(
        db,
        wedding_id,
    )


# ---------------------------------------------------------
# GET SINGLE GIFT
# GET /api/weddings/{wedding_id}/gifts/{gift_id}
# ---------------------------------------------------------

@router.get(
    "/{gift_id}",
    response_model=GiftResponse,
)
def get_gift_api(
    wedding_id: int,
    gift_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    gift = get_gift_by_id(
        db,
        gift_id,
        wedding_id,
    )

    if gift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift not found",
        )

    return gift


# ---------------------------------------------------------
# UPDATE GIFT
# PATCH /api/weddings/{wedding_id}/gifts/{gift_id}
# ---------------------------------------------------------

@router.patch(
    "/{gift_id}",
    response_model=GiftResponse,
)
def update_gift_api(
    wedding_id: int,
    gift_id: int,
    gift_data: GiftUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    gift = update_gift(
        db,
        gift_id,
        wedding_id,
        gift_data,
    )

    if gift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift not found",
        )

    return gift


# ---------------------------------------------------------
# DELETE GIFT
# DELETE /api/weddings/{wedding_id}/gifts/{gift_id}
# ---------------------------------------------------------

@router.delete(
    "/{gift_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_gift_api(
    wedding_id: int,
    gift_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    deleted = delete_gift(
        db,
        gift_id,
        wedding_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift not found",
        )

    return None