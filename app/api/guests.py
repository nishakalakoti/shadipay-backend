from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db
from app.services.wedding_service import get_wedding_by_id
from app.schemas.guest import (
    GuestCreate,
    GuestResponse,
    GuestUpdate,
)
from app.services.guest_service import (
    create_guest,
    get_guests,
    get_guest_by_id,
    update_guest,
    delete_guest,
)


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/guests",
    tags=["Guests"],
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
# CREATE GUEST
# POST /api/weddings/{wedding_id}/guests
# ---------------------------------------------------------

@router.post(
    "",
    response_model=GuestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_guest_api(
    wedding_id: int,
    guest_data: GuestCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return create_guest(
        db,
        wedding_id,
        guest_data,
    )


# ---------------------------------------------------------
# GET ALL GUESTS
# GET /api/weddings/{wedding_id}/guests
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[GuestResponse],
)
def get_guests_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return get_guests(
        db,
        wedding_id,
    )


# ---------------------------------------------------------
# GET SINGLE GUEST
# GET /api/weddings/{wedding_id}/guests/{guest_id}
# ---------------------------------------------------------

@router.get(
    "/{guest_id}",
    response_model=GuestResponse,
)
def get_guest_api(
    wedding_id: int,
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    guest = get_guest_by_id(
        db,
        guest_id,
        wedding_id,
    )

    if guest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    return guest


# ---------------------------------------------------------
# UPDATE GUEST
# PATCH /api/weddings/{wedding_id}/guests/{guest_id}
# ---------------------------------------------------------

@router.patch(
    "/{guest_id}",
    response_model=GuestResponse,
)
def update_guest_api(
    wedding_id: int,
    guest_id: int,
    guest_data: GuestUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    guest = update_guest(
        db,
        guest_id,
        wedding_id,
        guest_data,
    )

    if guest is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    return guest


# ---------------------------------------------------------
# DELETE GUEST
# DELETE /api/weddings/{wedding_id}/guests/{guest_id}
# ---------------------------------------------------------

@router.delete(
    "/{guest_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_guest_api(
    wedding_id: int,
    guest_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    deleted = delete_guest(
        db,
        guest_id,
        wedding_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guest not found",
        )

    return None