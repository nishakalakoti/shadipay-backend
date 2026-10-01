from datetime import datetime

from pydantic import BaseModel


class ActivityResponse(BaseModel):
    id: str
    type: str
    title: str
    description: str
    timestamp: datetime