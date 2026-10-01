from datetime import date, datetime

from pydantic import BaseModel


class QRCodeResponse(BaseModel):
    id: int
    wedding_id: int

    couple_name: str
    wedding_date: date | None
    wedding_venue: str | None

    registry_link: str

    qr_image_url: str

    created_at: datetime
    updated_at: datetime