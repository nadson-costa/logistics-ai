from datetime import datetime
from typing import List

from pydantic import BaseModel


class AlertOut(BaseModel):
    id: int
    event_type: str
    frame_index: int
    confidence: float
    class_id: int
    created_at: datetime


class AlertListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[AlertOut]
