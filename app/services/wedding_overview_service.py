from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.guest import Guest
from app.models.gift import Gift
from app.models.payment import Payment


def get_wedding_overview(
    db: Session,
    wedding_id: int,
):
    # =====================================================
    # TOTAL GUESTS
    # =====================================================

    total_guests = (
        db.query(func.count(Guest.id))
        .filter(
            Guest.wedding_id == wedding_id
        )
        .scalar()
        or 0
    )


    # =====================================================
    # TOTAL GIFTS AMOUNT
    # SUM OF GIFT AMOUNTS
    # =====================================================

    total_gifts = (
        db.query(func.sum(Gift.amount))
        .filter(
            Gift.wedding_id == wedding_id
        )
        .scalar()
        or 0
    )


    # =====================================================
    # ONLINE PAYMENTS
    # SUCCESSFUL PAYMENTS ONLY
    # =====================================================

    online_payments = (
        db.query(func.sum(Payment.amount))
        .filter(
            Payment.wedding_id == wedding_id,
            Payment.status == "Success",
        )
        .scalar()
        or 0
    )


    return {
        "wedding_id": wedding_id,
        "total_guests": int(total_guests),
        "total_gifts": int(total_gifts),
        "online_payments": int(online_payments),
    }