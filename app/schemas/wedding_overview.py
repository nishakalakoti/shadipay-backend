from pydantic import BaseModel


class WeddingOverviewResponse(BaseModel):
    wedding_id: int
    total_guests: int
    total_gifts: int
    online_payments: float