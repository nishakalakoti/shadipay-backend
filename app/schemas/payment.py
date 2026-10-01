from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# CREATE PAYMENT
# =====================================================

class PaymentCreate(BaseModel):

    guest_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    amount: int = Field(
        ...,
        ge=0,
    )

    method: str = Field(
        default="UPI",
        min_length=1,
        max_length=50,
    )

    status: str = Field(
        default="Success",
        min_length=1,
        max_length=20,
    )

    payment_date: datetime


# =====================================================
# UPDATE PAYMENT
# =====================================================

class PaymentUpdate(BaseModel):

    guest_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    amount: int | None = Field(
        default=None,
        ge=0,
    )

    method: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    payment_date: datetime | None = None


# =====================================================
# PAYMENT RESPONSE
# =====================================================

class PaymentResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    wedding_id: int
    gift_id: int | None

    transaction_id: str
    guest_name: str
    amount: int
    method: str
    status: str
    payment_date: datetime
    created_at: datetime
    updated_at: datetime