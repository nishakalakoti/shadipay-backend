from sqlalchemy.orm import Session

from app.models.guest import Guest
from app.models.gift import Gift


def get_recent_activities(
    db: Session,
    wedding_id: int,
    limit: int = 10,
) -> list[dict]:

    activities = []

    # ---------------------------------------------------------
    # GIFT ACTIVITIES
    # ---------------------------------------------------------

    gifts = (
        db.query(Gift)
        .filter(
            Gift.wedding_id == wedding_id
        )
        .order_by(
            Gift.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    for gift in gifts:
        if gift.gift_type.lower() == "physical":
            title = "Physical gift logged"
            description = (
                f"{gift.gift} from {gift.guest_name}"
            )

            activity_type = "physical_gift"

        else:
            title = (
                f"{gift.guest_name} sent a gift"
            )

            description = (
                f"₹{gift.amount:,}"
            )

            activity_type = "gift"

        activities.append(
            {
                "id": f"gift-{gift.id}",
                "type": activity_type,
                "title": title,
                "description": description,
                "timestamp": gift.created_at,
            }
        )

    # ---------------------------------------------------------
    # RSVP ACTIVITIES
    # ---------------------------------------------------------

    guests = (
        db.query(Guest)
        .filter(
            Guest.wedding_id == wedding_id
        )
        .order_by(
            Guest.updated_at.desc()
        )
        .limit(limit)
        .all()
    )

    for guest in guests:

        if guest.rsvp_status.lower() == "attending":
            rsvp_text = "Yes"

        elif guest.rsvp_status.lower() == "declined":
            rsvp_text = "No"

        else:
            rsvp_text = "Pending"

        activities.append(
            {
                "id": f"guest-{guest.id}",
                "type": "rsvp",
                "title": (
                    f"{guest.guest_name} RSVP'd "
                    f"{rsvp_text}"
                ),
                "description": guest.rsvp_status,
                "timestamp": guest.updated_at,
            }
        )

    # ---------------------------------------------------------
    # SORT ALL ACTIVITIES
    # ---------------------------------------------------------

    activities.sort(
        key=lambda activity: activity["timestamp"],
        reverse=True,
    )

    # ---------------------------------------------------------
    # LIMIT FINAL RESULT
    # ---------------------------------------------------------

    return activities[:limit]