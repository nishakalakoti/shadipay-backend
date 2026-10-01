from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.models.gift import Gift
from app.models.guest import Guest
from app.models.wedding import Wedding


# =========================================
# Period Helper
# =========================================

def get_period_dates(period: str):
    """
    Returns:
        start_date
        end_date
    """

    today = date.today()

    if period == "all_time":
        return None, None

    if period == "this_month":
        start_date = today.replace(day=1)
        return start_date, today

    if period == "last_3_months":
        start_date = today - timedelta(days=90)
        return start_date, today

    if period == "this_year":
        start_date = today.replace(month=1, day=1)
        return start_date, today

    raise ValueError(
        "Invalid period. Use: all_time, this_month, last_3_months, this_year."
    )


# =========================================
# PAYMENT REPORT
# =========================================

def get_payment_report(
    db: Session,
    wedding_id: int,
    period: str = "all_time",
):
    start_date, end_date = get_period_dates(period)

    query = (
        db.query(Gift)
        .filter(
            Gift.wedding_id == wedding_id,
            Gift.gift_type == "Online",
        )
    )

    if start_date and end_date:
        query = query.filter(
            Gift.gift_date >= start_date,
            Gift.gift_date <= end_date,
        )

    gifts = query.order_by(
        Gift.gift_date.desc(),
        Gift.id.desc(),
    ).all()

    payments = []

    for gift in gifts:
        payment_date = datetime.combine(
            gift.gift_date,
            datetime.min.time(),
        )

        payments.append(
            {
                "id": gift.id,
                "transaction_id": f"GIFT-{gift.id:06d}",
                "guest_name": gift.guest_name,
                "amount": gift.amount,
                "method": "UPI",
                "status": "Success",
                "payment_date": payment_date,
            }
        )

    total_amount = sum(
        payment["amount"] for payment in payments
    )

    return {
        "report_type": "Payment Report",
        "period": period,
        "total_payments": len(payments),
        "total_amount": total_amount,
        "payments": payments,
    }


# =========================================
# GIFT REPORT
# =========================================

def get_gift_report(
    db: Session,
    wedding_id: int,
    period: str = "all_time",
):
    start_date, end_date = get_period_dates(period)

    query = db.query(Gift).filter(
        Gift.wedding_id == wedding_id
    )

    if start_date and end_date:
        query = query.filter(
            Gift.gift_date >= start_date,
            Gift.gift_date <= end_date,
        )

    gifts = query.order_by(
        Gift.gift_date.desc(),
        Gift.id.desc(),
    ).all()

    gift_items = [
        {
            "id": gift.id,
            "guest_name": gift.guest_name,
            "gift": gift.gift,
            "gift_type": gift.gift_type,
            "amount": gift.amount,
            "gift_date": gift.gift_date,
        }
        for gift in gifts
    ]

    online_gifts = [
        gift for gift in gifts
        if gift.gift_type == "Online"
    ]

    physical_gifts = [
        gift for gift in gifts
        if gift.gift_type == "Physical"
    ]

    total_amount = sum(
        gift.amount for gift in gifts
    )

    return {
        "report_type": "Gift Report",
        "period": period,
        "total_gifts": len(gifts),
        "total_amount": total_amount,
        "online_gifts": len(online_gifts),
        "physical_gifts": len(physical_gifts),
        "gifts": gift_items,
    }


# =========================================
# GUEST REPORT
# =========================================

def get_guest_report(
    db: Session,
    wedding_id: int,
    period: str = "all_time",
):
    guests = (
        db.query(Guest)
        .filter(
            Guest.wedding_id == wedding_id
        )
        .order_by(Guest.id.asc())
        .all()
    )

    guest_items = [
        {
            "id": guest.id,
            "guest_name": guest.guest_name,
            "phone": guest.phone,
            "email": guest.email,
            "relation": guest.relation,
            "rsvp_status": guest.rsvp_status,
            "gift_amount": guest.gift_amount,
        }
        for guest in guests
    ]

    attending = len(
        [
            guest
            for guest in guests
            if guest.rsvp_status == "Attending"
        ]
    )

    pending = len(
        [
            guest
            for guest in guests
            if guest.rsvp_status == "Pending"
        ]
    )

    declined = len(
        [
            guest
            for guest in guests
            if guest.rsvp_status == "Declined"
        ]
    )

    return {
        "report_type": "Guest Report",
        "period": period,
        "total_guests": len(guests),
        "attending": attending,
        "pending": pending,
        "declined": declined,
        "guests": guest_items,
    }


# =========================================
# WEDDING SUMMARY
# =========================================

def get_wedding_summary(
    db: Session,
    wedding_id: int,
    period: str = "all_time",
):
    wedding = (
        db.query(Wedding)
        .filter(
            Wedding.id == wedding_id
        )
        .first()
    )

    if wedding is None:
        return None

    gift_report = get_gift_report(
        db,
        wedding_id,
        period,
    )

    payment_report = get_payment_report(
        db,
        wedding_id,
        period,
    )

    guest_report = get_guest_report(
        db,
        wedding_id,
        period,
    )

    return {
        "report_type": "Wedding Summary",
        "period": period,

        "wedding_id": wedding.id,
        "first_partner": wedding.first_partner,
        "second_partner": wedding.second_partner,
        "wedding_date": wedding.wedding_date,
        "wedding_venue": wedding.wedding_venue,

        "total_guests": guest_report["total_guests"],

        "total_gifts": gift_report["total_gifts"],
        "online_gifts": gift_report["online_gifts"],
        "physical_gifts": gift_report["physical_gifts"],
        "total_gift_amount": gift_report["total_amount"],

        "total_payments": payment_report["total_payments"],
        "total_payment_amount": payment_report["total_amount"],
    }