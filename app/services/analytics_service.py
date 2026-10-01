from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.guest import Guest
from app.models.gift import Gift
from app.schemas.analytics import (
    AnalyticsResponse,
    GiftDistribution,
    GuestActivity,
    PaymentOverviewItem,
)


def get_wedding_analytics(
    db: Session,
    wedding_id: int,
) -> AnalyticsResponse:

    # ---------------------------------------------------------
    # GIFT SUMMARY
    # ---------------------------------------------------------

    total_gifts = (
        db.query(
            func.coalesce(
                func.sum(Gift.amount),
                0,
            )
        )
        .filter(
            Gift.wedding_id == wedding_id
        )
        .scalar()
    )

    online_payments = (
        db.query(
            func.coalesce(
                func.sum(Gift.amount),
                0,
            )
        )
        .filter(
            Gift.wedding_id == wedding_id,
            func.lower(Gift.gift_type) == "online",
        )
        .scalar()
    )

    physical_gifts = (
        db.query(func.count(Gift.id))
        .filter(
            Gift.wedding_id == wedding_id,
            func.lower(Gift.gift_type) == "physical",
        )
        .scalar()
    )

    # ---------------------------------------------------------
    # GIFT DISTRIBUTION
    # ---------------------------------------------------------

    total_gift_count = (
        db.query(func.count(Gift.id))
        .filter(
            Gift.wedding_id == wedding_id
        )
        .scalar()
    )

    online_gift_count = (
        db.query(func.count(Gift.id))
        .filter(
            Gift.wedding_id == wedding_id,
            func.lower(Gift.gift_type) == "online",
        )
        .scalar()
    )

    physical_gift_count = (
        db.query(func.count(Gift.id))
        .filter(
            Gift.wedding_id == wedding_id,
            func.lower(Gift.gift_type) == "physical",
        )
        .scalar()
    )

    if total_gift_count:
        online_percentage = round(
            (online_gift_count / total_gift_count) * 100,
            2,
        )

        physical_percentage = round(
            (physical_gift_count / total_gift_count) * 100,
            2,
        )
    else:
        online_percentage = 0
        physical_percentage = 0

    # ---------------------------------------------------------
    # GUEST SUMMARY
    # ---------------------------------------------------------

    total_guests = (
        db.query(func.count(Guest.id))
        .filter(
            Guest.wedding_id == wedding_id
        )
        .scalar()
    )

    attending = (
        db.query(func.count(Guest.id))
        .filter(
            Guest.wedding_id == wedding_id,
            func.lower(Guest.rsvp_status) == "attending",
        )
        .scalar()
    )

    pending = (
        db.query(func.count(Guest.id))
        .filter(
            Guest.wedding_id == wedding_id,
            func.lower(Guest.rsvp_status) == "pending",
        )
        .scalar()
    )

    declined = (
        db.query(func.count(Guest.id))
        .filter(
            Guest.wedding_id == wedding_id,
            func.lower(Guest.rsvp_status) == "declined",
        )
        .scalar()
    )

    if total_guests:
        attending_percentage = round(
            (attending / total_guests) * 100,
            2,
        )

        pending_percentage = round(
            (pending / total_guests) * 100,
            2,
        )

        declined_percentage = round(
            (declined / total_guests) * 100,
            2,
        )
    else:
        attending_percentage = 0
        pending_percentage = 0
        declined_percentage = 0

    # ---------------------------------------------------------
    # PAYMENT OVERVIEW - LAST 7 DAYS
    # ---------------------------------------------------------

    today = date.today()
    start_date = today - timedelta(days=6)

    daily_payments = (
        db.query(
            Gift.gift_date,
            func.coalesce(
                func.sum(Gift.amount),
                0,
            ),
        )
        .filter(
            Gift.wedding_id == wedding_id,
            func.lower(Gift.gift_type) == "online",
            Gift.gift_date >= start_date,
            Gift.gift_date <= today,
        )
        .group_by(
            Gift.gift_date
        )
        .order_by(
            Gift.gift_date.asc()
        )
        .all()
    )

    payment_map = {
        payment_date: amount
        for payment_date, amount in daily_payments
    }

    payment_overview = []

    for day_number in range(7):
        current_date = start_date + timedelta(
            days=day_number
        )

        payment_overview.append(
            PaymentOverviewItem(
                date=current_date,
                amount=int(
                    payment_map.get(
                        current_date,
                        0,
                    )
                ),
            )
        )

    # ---------------------------------------------------------
    # FINAL RESPONSE
    # ---------------------------------------------------------

    return AnalyticsResponse(
        total_gifts=int(total_gifts or 0),
        online_payments=int(online_payments or 0),
        physical_gifts=int(physical_gifts or 0),
        total_guests=int(total_guests or 0),
        payment_overview=payment_overview,
        gift_distribution=GiftDistribution(
            online_percentage=online_percentage,
            physical_percentage=physical_percentage,
        ),
        guest_activity=GuestActivity(
            total_guests=int(total_guests or 0),
            attending=int(attending or 0),
            attending_percentage=attending_percentage,
            pending=int(pending or 0),
            pending_percentage=pending_percentage,
            declined=int(declined or 0),
            declined_percentage=declined_percentage,
        ),
    )