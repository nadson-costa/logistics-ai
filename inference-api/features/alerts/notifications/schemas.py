from datetime import datetime
from typing import List

from pydantic import BaseModel


class AlertSummary(BaseModel):
    window_start: datetime
    window_end: datetime
    total_alerts: int
    avg_confidence: float
    min_confidence: float
    class_ids: List[int]
