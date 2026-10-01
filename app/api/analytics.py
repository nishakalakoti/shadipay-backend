from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import get_wedding_analytics
from app.services.wedding_service import get_wedding_by_id


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/analytics",
    tags=["Analytics"],
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
# GET WEDDING ANALYTICS
# GET /api/weddings/{wedding_id}/analytics
# ---------------------------------------------------------

@router.get(
    "",
    response_model=AnalyticsResponse,
)
def get_analytics_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return get_wedding_analytics(
        db,
        wedding_id,
    )