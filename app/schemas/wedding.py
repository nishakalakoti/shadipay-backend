from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class WeddingCreate(BaseModel):
    first_partner: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    second_partner: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    wedding_date: date

    wedding_venue: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )


class WeddingUpdate(BaseModel):
    first_partner: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    second_partner: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    wedding_date: date | None = None

    wedding_venue: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class WeddingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    firebase_uid: str
    first_partner: str
    second_partner: str
    wedding_date: date
    wedding_venue: str
    created_at: datetime
    updated_at: datetime