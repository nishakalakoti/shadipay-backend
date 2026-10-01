from sqlalchemy.orm import Session

from app.models.gift import Gift
from app.schemas.gift import GiftCreate, GiftUpdate


# =====================================================
# CREATE GIFT
# =====================================================

def create_gift(
    db: Session,
    wedding_id: int,
    gift_data: GiftCreate,
) -> Gift:

    gift = Gift(
        wedding_id=wedding_id,
        guest_name=gift_data.guest_name,
        gift=gift_data.gift,
        gift_type=gift_data.gift_type,
        amount=gift_data.amount,
        gift_date=gift_data.gift_date,
    )

    db.add(gift)
    db.commit()
    db.refresh(gift)

    return gift


# =====================================================
# GET ALL GIFTS
# =====================================================

def get_gifts(
    db: Session,
    wedding_id: int,
) -> list[Gift]:

    return (
        db.query(Gift)
        .filter(
            Gift.wedding_id == wedding_id
        )
        .order_by(
            Gift.id.asc()
        )
        .all()
    )


# =====================================================
# GET SINGLE GIFT
# =====================================================

def get_gift_by_id(
    db: Session,
    gift_id: int,
    wedding_id: int,
) -> Gift | None:

    return (
        db.query(Gift)
        .filter(
            Gift.id == gift_id,
            Gift.wedding_id == wedding_id,
        )
        .first()
    )


# =====================================================
# UPDATE GIFT
# =====================================================

def update_gift(
    db: Session,
    gift_id: int,
    wedding_id: int,
    gift_data: GiftUpdate,
) -> Gift | None:

    gift = (
        db.query(Gift)
        .filter(
            Gift.id == gift_id,
            Gift.wedding_id == wedding_id,
        )
        .first()
    )

    if gift is None:
        return None

    update_data = gift_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            gift,
            field,
            value
        )

    db.commit()
    db.refresh(gift)

    return gift


# =====================================================
# DELETE GIFT
# =====================================================

def delete_gift(
    db: Session,
    gift_id: int,
    wedding_id: int,
) -> bool:

    gift = (
        db.query(Gift)
        .filter(
            Gift.id == gift_id,
            Gift.wedding_id == wedding_id,
        )
        .first()
    )

    if gift is None:
        return False

    db.delete(gift)
    db.commit()

    return True