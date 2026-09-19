from typing import Protocol

from .schemas import AlertSummary


class NotificationChannel(Protocol):
    async def send(self, summary: AlertSummary) -> None:
        ...
