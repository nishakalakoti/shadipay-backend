from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.api.auth import get_current_user

from app.schemas.wedding_overview import (
    WeddingOverviewResponse
)

from app.services.wedding_overview_service import (
    get_wedding_overview
)

from app.services.wedding_service import (
    get_wedding_by_id
)


router = APIRouter(
    prefix="/api/weddings/{wedding_id}",
    tags=["Wedding Overview"],
)


# =========================================================
# WEDDING ACCESS CHECK
# =========================================================

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


# =========================================================
# GET WEDDING OVERVIEW
# GET /api/weddings/{wedding_id}/overview
# =========================================================

@router.get(
    "/overview",
    response_model=WeddingOverviewResponse,
)
def wedding_overview(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return get_wedding_overview(
        db=db,
        wedding_id=wedding_id,
    )