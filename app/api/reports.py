from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db

from app.schemas.reports import (
    PaymentReportResponse,
    GiftReportResponse,
    GuestReportResponse,
    WeddingSummaryResponse,
)

from app.services.report_service import (
    get_payment_report,
    get_gift_report,
    get_guest_report,
    get_wedding_summary,
)

from app.services.wedding_service import (
    get_wedding_by_id,
)


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/reports",
    tags=["Reports"],
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
# GET PAYMENT REPORT
# GET /api/weddings/{wedding_id}/reports/payments
# =====================================================

@router.get(
    "/payments",
    response_model=PaymentReportResponse,
)
def get_payment_report_api(
    wedding_id: int,
    period: str = Query(
        default="all_time",
    ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    try:
        return get_payment_report(
            db,
            wedding_id,
            period,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# =====================================================
# GET GIFT REPORT
# GET /api/weddings/{wedding_id}/reports/gifts
# =====================================================

@router.get(
    "/gifts",
    response_model=GiftReportResponse,
)
def get_gift_report_api(
    wedding_id: int,
    period: str = Query(
        default="all_time",
    ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    try:
        return get_gift_report(
            db,
            wedding_id,
            period,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# =====================================================
# GET GUEST REPORT
# GET /api/weddings/{wedding_id}/reports/guests
# =====================================================

@router.get(
    "/guests",
    response_model=GuestReportResponse,
)
def get_guest_report_api(
    wedding_id: int,
    period: str = Query(
        default="all_time",
    ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    try:
        return get_guest_report(
            db,
            wedding_id,
            period,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


# =====================================================
# GET WEDDING SUMMARY
# GET /api/weddings/{wedding_id}/reports/summary
# =====================================================

@router.get(
    "/summary",
    response_model=WeddingSummaryResponse,
)
def get_wedding_summary_api(
    wedding_id: int,
    period: str = Query(
        default="all_time",
    ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    try:
        result = get_wedding_summary(
            db,
            wedding_id,
            period,
        )

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wedding not found",
            )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )