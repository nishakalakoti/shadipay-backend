from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class GuestCreate(BaseModel):
    guest_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    phone: str = Field(
        ...,
        min_length=7,
        max_length=20,
    )

    email: EmailStr

    relation: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )

    rsvp_status: str = Field(
        default="Pending",
        min_length=1,
        max_length=20,
    )

    gift_amount: int = Field(
        default=0,
        ge=0,
    )


class GuestUpdate(BaseModel):
    guest_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )

    email: EmailStr | None = None

    relation: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    rsvp_status: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    gift_amount: int | None = Field(
        default=None,
        ge=0,
    )


class GuestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    wedding_id: int
    guest_name: str
    phone: str
    email: EmailStr
    relation: str
    rsvp_status: str
    gift_amount: int
    created_at: datetime
    updated_at: datetime