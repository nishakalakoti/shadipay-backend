from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InvitationCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    message: str = Field(
        ...,
        min_length=1,
    )

    theme: str = Field(
        default="Classic",
        min_length=1,
        max_length=50,
    )


class InvitationUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    message: str | None = Field(
        default=None,
        min_length=1,
    )

    theme: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )


class InvitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    wedding_id: int
    title: str
    message: str
    theme: str
    slug: str
    invitation_url: str
    created_at: datetime
    updated_at: datetime