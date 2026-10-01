from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db
from app.schemas.activity import ActivityResponse
from app.services.activity_service import get_recent_activities
from app.services.wedding_service import get_wedding_by_id


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/activities",
    tags=["Activities"],
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
# GET RECENT ACTIVITIES
# GET /api/weddings/{wedding_id}/activities
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[ActivityResponse],
)
def get_activities_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    return get_recent_activities(
        db,
        wedding_id,
    )