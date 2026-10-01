from sqlalchemy.orm import Session

from app.models.wedding import Wedding
from app.schemas.wedding import WeddingCreate, WeddingUpdate


def create_wedding(
    db: Session,
    wedding_data: WeddingCreate,
    firebase_uid: str,
) -> Wedding:

    wedding = Wedding(
        firebase_uid=firebase_uid,
        first_partner=wedding_data.first_partner,
        second_partner=wedding_data.second_partner,
        wedding_date=wedding_data.wedding_date,
        wedding_venue=wedding_data.wedding_venue,
    )

    db.add(wedding)
    db.commit()
    db.refresh(wedding)

    return wedding


def get_weddings(
    db: Session,
    firebase_uid: str,
) -> list[Wedding]:

    return (
        db.query(Wedding)
        .filter(
            Wedding.firebase_uid == firebase_uid
        )
        .order_by(Wedding.id.asc())
        .all()
    )


def get_wedding_by_id(
    db: Session,
    wedding_id: int,
    firebase_uid: str,
) -> Wedding | None:

    return (
        db.query(Wedding)
        .filter(
            Wedding.id == wedding_id,
            Wedding.firebase_uid == firebase_uid,
        )
        .first()
    )


def update_wedding(
    db: Session,
    wedding_id: int,
    wedding_data: WeddingUpdate,
    firebase_uid: str,
) -> Wedding | None:

    wedding = (
        db.query(Wedding)
        .filter(
            Wedding.id == wedding_id,
            Wedding.firebase_uid == firebase_uid,
        )
        .first()
    )

    if wedding is None:
        return None

    update_data = wedding_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(wedding, field, value)

    db.commit()
    db.refresh(wedding)

    return wedding


def delete_wedding(
    db: Session,
    wedding_id: int,
    firebase_uid: str,
) -> bool:

    wedding = (
        db.query(Wedding)
        .filter(
            Wedding.id == wedding_id,
            Wedding.firebase_uid == firebase_uid,
        )
        .first()
    )

    if wedding is None:
        return False

    db.delete(wedding)
    db.commit()

    return True