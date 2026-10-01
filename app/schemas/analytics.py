from datetime import date

from pydantic import BaseModel


class PaymentOverviewItem(BaseModel):
    date: date
    amount: int


class GiftDistribution(BaseModel):
    online_percentage: float
    physical_percentage: float


class GuestActivity(BaseModel):
    total_guests: int

    attending: int
    attending_percentage: float

    pending: int
    pending_percentage: float

    declined: int
    declined_percentage: float


class AnalyticsResponse(BaseModel):
    total_gifts: int
    online_payments: int
    physical_gifts: int
    total_guests: int

    payment_overview: list[PaymentOverviewItem]

    gift_distribution: GiftDistribution

    guest_activity: GuestActivity