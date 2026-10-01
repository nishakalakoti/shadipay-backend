from sqlalchemy.orm import Session

from app.models.guest import Guest
from app.schemas.guest import GuestCreate, GuestUpdate


def create_guest(
    db: Session,
    wedding_id: int,
    guest_data: GuestCreate,
) -> Guest:

    guest = Guest(
        wedding_id=wedding_id,
        guest_name=guest_data.guest_name,
        phone=guest_data.phone,
        email=guest_data.email,
        relation=guest_data.relation,
        rsvp_status=guest_data.rsvp_status,
        gift_amount=guest_data.gift_amount,
    )

    db.add(guest)
    db.commit()
    db.refresh(guest)

    return guest


def get_guests(
    db: Session,
    wedding_id: int,
) -> list[Guest]:

    return (
        db.query(Guest)
        .filter(
            Guest.wedding_id == wedding_id
        )
        .order_by(Guest.id.asc())
        .all()
    )


def get_guest_by_id(
    db: Session,
    guest_id: int,
    wedding_id: int,
) -> Guest | None:

    return (
        db.query(Guest)
        .filter(
            Guest.id == guest_id,
            Guest.wedding_id == wedding_id,
        )
        .first()
    )


def update_guest(
    db: Session,
    guest_id: int,
    wedding_id: int,
    guest_data: GuestUpdate,
) -> Guest | None:

    guest = (
        db.query(Guest)
        .filter(
            Guest.id == guest_id,
            Guest.wedding_id == wedding_id,
        )
        .first()
    )

    if guest is None:
        return None

    update_data = guest_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(guest, field, value)

    db.commit()
    db.refresh(guest)

    return guest


def delete_guest(
    db: Session,
    guest_id: int,
    wedding_id: int,
) -> bool:

    guest = (
        db.query(Guest)
        .filter(
            Guest.id == guest_id,
            Guest.wedding_id == wedding_id,
        )
        .first()
    )

    if guest is None:
        return False

    db.delete(guest)
    db.commit()

    return True