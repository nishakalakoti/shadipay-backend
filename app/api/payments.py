from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db

from app.schemas.payment import (
    PaymentResponse,
    PaymentUpdate,
)

from app.services.payment_service import (
    get_payments,
    get_payment_by_id,
    update_payment,
    delete_payment,
)

from app.services.wedding_service import (
    get_wedding_by_id,
)


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/payments",
    tags=["Payments"],
)


# =====================================================
# VERIFY WEDDING ACCESS
# =====================================================

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


# =====================================================
# GET ALL PAYMENTS
# GET /api/weddings/{wedding_id}/payments
# =====================================================

@router.get(
    "",
    response_model=list[PaymentResponse],
)
def get_payments_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return get_payments(
        db,
        wedding_id,
    )


# =====================================================
# GET SINGLE PAYMENT
# GET /api/weddings/{wedding_id}/payments/{payment_id}
# =====================================================

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def get_payment_api(
    wedding_id: int,
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    payment = get_payment_by_id(
        db,
        payment_id,
        wedding_id,
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return payment


# =====================================================
# UPDATE PAYMENT
# PATCH /api/weddings/{wedding_id}/payments/{payment_id}
# =====================================================

@router.patch(
    "/{payment_id}",
    response_model=PaymentResponse,
)
def update_payment_api(
    wedding_id: int,
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    payment = update_payment(
        db,
        payment_id,
        wedding_id,
        payment_data,
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return payment


# =====================================================
# DELETE PAYMENT
# DELETE /api/weddings/{wedding_id}/payments/{payment_id}
# =====================================================

@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_payment_api(
    wedding_id: int,
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    deleted = delete_payment(
        db,
        payment_id,
        wedding_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return None