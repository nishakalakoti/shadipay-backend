from datetime import date, datetime
from pydantic import BaseModel


# =========================================
# Payment Report
# =========================================

class PaymentReportItem(BaseModel):
    id: int
    transaction_id: str
    guest_name: str
    amount: int
    method: str
    status: str
    payment_date: datetime


class PaymentReportResponse(BaseModel):
    report_type: str
    period: str
    total_payments: int
    total_amount: int
    payments: list[PaymentReportItem]


# =========================================
# Gift Report
# =========================================

class GiftReportItem(BaseModel):
    id: int
    guest_name: str
    gift: str
    gift_type: str
    amount: int
    gift_date: date


class GiftReportResponse(BaseModel):
    report_type: str
    period: str
    total_gifts: int
    total_amount: int
    online_gifts: int
    physical_gifts: int
    gifts: list[GiftReportItem]


# =========================================
# Guest Report
# =========================================

class GuestReportItem(BaseModel):
    id: int
    guest_name: str
    phone: str | None
    email: str | None
    relation: str | None
    rsvp_status: str
    gift_amount: int


class GuestReportResponse(BaseModel):
    report_type: str
    period: str
    total_guests: int
    attending: int
    pending: int
    declined: int
    guests: list[GuestReportItem]


# =========================================
# Wedding Summary
# =========================================

class WeddingSummaryResponse(BaseModel):
    report_type: str
    period: str

    wedding_id: int
    first_partner: str
    second_partner: str
    wedding_date: date | None
    wedding_venue: str | None

    total_guests: int

    total_gifts: int
    online_gifts: int
    physical_gifts: int
    total_gift_amount: int

    total_payments: int
    total_payment_amount: int