from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.api.weddings import get_db
from app.services.wedding_service import get_wedding_by_id
from app.schemas.invitation import (
    InvitationCreate,
    InvitationResponse,
    InvitationUpdate,
)
from app.services.invitation_service import (
    create_invitation,
    get_invitation_url,
    get_invitations,
    get_invitation_by_id,
    update_invitation,
    delete_invitation,
)


router = APIRouter(
    prefix="/api/weddings/{wedding_id}/invitations",
    tags=["Invitations"],
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


def invitation_response(
    invitation,
) -> dict:
    return {
        "id": invitation.id,
        "wedding_id": invitation.wedding_id,
        "title": invitation.title,
        "message": invitation.message,
        "theme": invitation.theme,
        "slug": invitation.slug,
        "invitation_url": get_invitation_url(invitation),
        "created_at": invitation.created_at,
        "updated_at": invitation.updated_at,
    }


# ---------------------------------------------------------
# CREATE INVITATION
# POST /api/weddings/{wedding_id}/invitations
# ---------------------------------------------------------

@router.post(
    "",
    response_model=InvitationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_invitation_api(
    wedding_id: int,
    invitation_data: InvitationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    wedding = verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    wedding_slug = (
        f"{wedding.first_partner}-{wedding.second_partner}"
    )

    invitation = create_invitation(
        db,
        wedding_id,
        invitation_data,
        wedding_slug,
    )

    return invitation_response(invitation)


# ---------------------------------------------------------
# GET ALL INVITATIONS
# GET /api/weddings/{wedding_id}/invitations
# ---------------------------------------------------------

@router.get(
    "",
    response_model=list[InvitationResponse],
)
def get_invitations_api(
    wedding_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    invitations = get_invitations(
        db,
        wedding_id,
    )

    return [
        invitation_response(invitation)
        for invitation in invitations
    ]


# ---------------------------------------------------------
# GET SINGLE INVITATION
# GET /api/weddings/{wedding_id}/invitations/{invitation_id}
# ---------------------------------------------------------

@router.get(
    "/{invitation_id}",
    response_model=InvitationResponse,
)
def get_invitation_api(
    wedding_id: int,
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    invitation = get_invitation_by_id(
        db,
        invitation_id,
        wedding_id,
    )

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    return invitation_response(invitation)


# ---------------------------------------------------------
# UPDATE INVITATION
# PATCH /api/weddings/{wedding_id}/invitations/{invitation_id}
# ---------------------------------------------------------

@router.patch(
    "/{invitation_id}",
    response_model=InvitationResponse,
)
def update_invitation_api(
    wedding_id: int,
    invitation_id: int,
    invitation_data: InvitationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    invitation = update_invitation(
        db,
        invitation_id,
        wedding_id,
        invitation_data,
    )

    if invitation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    return invitation_response(invitation)


# ---------------------------------------------------------
# DELETE INVITATION
# DELETE /api/weddings/{wedding_id}/invitations/{invitation_id}
# ---------------------------------------------------------

@router.delete(
    "/{invitation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_invitation_api(
    wedding_id: int,
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    verify_wedding_access(
        wedding_id,
        db,
        current_user,
    )

    deleted = delete_invitation(
        db,
        invitation_id,
        wedding_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    return None