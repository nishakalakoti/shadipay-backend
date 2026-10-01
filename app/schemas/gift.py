from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# =====================================================
# CREATE GIFT
# =====================================================

class GiftCreate(BaseModel):

    guest_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    gift: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    gift_type: Literal[
        "Physical",
        "Online",
    ]

    amount: int = Field(
        default=0,
        ge=0,
    )

    gift_date: date


# =====================================================
# UPDATE GIFT
# =====================================================

class GiftUpdate(BaseModel):

    guest_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    gift: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    gift_type: Literal[
        "Physical",
        "Online",
    ] | None = None

    amount: int | None = Field(
        default=None,
        ge=0,
    )

    gift_date: date | None = None


# =====================================================
# GIFT RESPONSE
# =====================================================

class GiftResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    wedding_id: int
    guest_name: str
    gift: str
    gift_type: str
    amount: int
    gift_date: date
    created_at: datetime
    updated_at: datetime