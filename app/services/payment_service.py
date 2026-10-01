from datetime import datetime, time, timezone

from sqlalchemy.orm import Session

from app.models.gift import Gift
from app.schemas.payment import PaymentUpdate


# =====================================================
# PAYMENT DATE
# =====================================================

def get_payment_datetime(gift_date):
    return datetime.combine(
        gift_date,
        time.min,
        tzinfo=timezone.utc,
    )


# =====================================================
# CONVERT ONLINE GIFT → PAYMENT RESPONSE
# =====================================================

def gift_to_payment(gift: Gift) -> dict:
    return {
        "id": gift.id,
        "wedding_id": gift.wedding_id,
        "gift_id": gift.id,
        "transaction_id": f"GIFT-{gift.id:06d}",
        "guest_name": gift.guest_name,
        "amount": gift.amount,
        "method": "UPI",
        "status": "Success",
        "payment_date": get_payment_datetime(
            gift.gift_date
        ),
        "created_at": gift.created_at,
        "updated_at": gift.updated_at,
    }


# =====================================================
# GET ALL PAYMENTS
# PAYMENTS COME FROM ONLINE GIFTS
# =====================================================

def get_payments(
    db: Session,
    wedding_id: int,
) -> list[dict]:

    gifts = (
        db.query(Gift)
        .filter(
            Gift.wedding_id == wedding_id,
            Gift.gift_type == "Online",
        )
        .order_by(
            Gift.gift_date.desc(),
            Gift.id.desc(),
        )
        .all()
    )

    return [
        gift_to_payment(gift)
        for gift in gifts
    ]


# =====================================================
# GET SINGLE PAYMENT
# PAYMENT ID = GIFT ID
# =====================================================

def get_payment_by_id(
    db: Session,
    payment_id: int,
    wedding_id: int,
) -> dict | None:

    gift = (
        db.query(Gift)
        .filter(
            Gift.id == payment_id,
            Gift.wedding_id == wedding_id,
            Gift.gift_type == "Online",
        )
        .first()
    )

    if gift is None:
        return None

    return gift_to_payment(gift)


# =====================================================
# UPDATE PAYMENT
# UPDATES THE LINKED ONLINE GIFT
# =====================================================

def update_payment(
    db: Session,
    payment_id: int,
    wedding_id: int,
    payment_data: PaymentUpdate,
) -> dict | None:

    gift = (
        db.query(Gift)
        .filter(
            Gift.id == payment_id,
            Gift.wedding_id == wedding_id,
            Gift.gift_type == "Online",
        )
        .first()
    )

    if gift is None:
        return None


    # -------------------------------------------------
    # UPDATE ONLY FIELDS THAT BELONG TO GIFT
    # -------------------------------------------------

    update_data = payment_data.model_dump(
        exclude_unset=True
    )

    if "guest_name" in update_data:
        gift.guest_name = update_data["guest_name"]

    if "amount" in update_data:
        gift.amount = update_data["amount"]

    if "payment_date" in update_data:
        gift.gift_date = update_data[
            "payment_date"
        ].date()


    db.commit()
    db.refresh(gift)

    return gift_to_payment(gift)


# =====================================================
# DELETE PAYMENT
# DELETE THE SOURCE ONLINE GIFT
# =====================================================

def delete_payment(
    db: Session,
    payment_id: int,
    wedding_id: int,
) -> bool:

    gift = (
        db.query(Gift)
        .filter(
            Gift.id == payment_id,
            Gift.wedding_id == wedding_id,
            Gift.gift_type == "Online",
        )
        .first()
    )

    if gift is None:
        return False


    db.delete(gift)
    db.commit()

    return True