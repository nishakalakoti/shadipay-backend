import secrets
import re

from sqlalchemy.orm import Session

from app.models.invitation import Invitation
from app.schemas.invitation import (
    InvitationCreate,
    InvitationUpdate,
)


def create_invitation(
    db: Session,
    wedding_id: int,
    invitation_data: InvitationCreate,
    wedding_slug: str,
) -> Invitation:

    base_slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        wedding_slug.lower(),
    ).strip("-")

    unique_code = secrets.token_hex(4)

    slug = f"{base_slug}-{unique_code}"

    invitation = Invitation(
        wedding_id=wedding_id,
        title=invitation_data.title,
        message=invitation_data.message,
        theme=invitation_data.theme,
        slug=slug,
    )

    db.add(invitation)
    db.commit()
    db.refresh(invitation)

    return invitation


def get_invitation_url(
    invitation: Invitation,
) -> str:

    return f"http://localhost:3000/invitation/{invitation.slug}"


def get_invitations(
    db: Session,
    wedding_id: int,
) -> list[Invitation]:

    return (
        db.query(Invitation)
        .filter(
            Invitation.wedding_id == wedding_id
        )
        .order_by(Invitation.id.asc())
        .all()
    )


def get_invitation_by_id(
    db: Session,
    invitation_id: int,
    wedding_id: int,
) -> Invitation | None:

    return (
        db.query(Invitation)
        .filter(
            Invitation.id == invitation_id,
            Invitation.wedding_id == wedding_id,
        )
        .first()
    )


def update_invitation(
    db: Session,
    invitation_id: int,
    wedding_id: int,
    invitation_data: InvitationUpdate,
) -> Invitation | None:

    invitation = (
        db.query(Invitation)
        .filter(
            Invitation.id == invitation_id,
            Invitation.wedding_id == wedding_id,
        )
        .first()
    )

    if invitation is None:
        return None

    update_data = invitation_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(invitation, field, value)

    db.commit()
    db.refresh(invitation)

    return invitation


def delete_invitation(
    db: Session,
    invitation_id: int,
    wedding_id: int,
) -> bool:

    invitation = (
        db.query(Invitation)
        .filter(
            Invitation.id == invitation_id,
            Invitation.wedding_id == wedding_id,
        )
        .first()
    )

    if invitation is None:
        return False

    db.delete(invitation)
    db.commit()

    return True