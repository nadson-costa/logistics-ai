import asyncio
from datetime import datetime, timezone
from typing import List

from features.alerts.repository import AlertRepository

from .base import NotificationChannel
from .schemas import AlertSummary


class NotificationDispatcher:
    def __init__(
        self,
        repository: AlertRepository,
        channels: List[NotificationChannel],
        window_seconds: int,
    ):
        self.repository = repository
        self.channels = channels
        self.window_seconds = window_seconds

    @staticmethod
    def _now() -> datetime:
        # naive, mas sempre UTC: a coluna created_at é TIMESTAMP (sem timezone),
        # e o asyncpg rejeita comparar datetime "aware" com coluna "naive".
        return datetime.now(timezone.utc).replace(tzinfo=None)

    async def run(self):
        last_check = self._now()

        while True:
            await asyncio.sleep(self.window_seconds)

            window_start = last_check
            window_end = self._now()
            last_check = window_end

            try:
                stats = await self.repository.get_alert_stats_since(window_start)
            except Exception as e:
                print(f"ERRO: Falha ao consultar resumo de alertas: {e}")
                continue

            if stats is None or stats["total_alerts"] == 0:
                continue

            summary = AlertSummary(
                window_start=window_start,
                window_end=window_end,
                total_alerts=stats["total_alerts"],
                avg_confidence=float(stats["avg_confidence"]),
                min_confidence=float(stats["min_confidence"]),
                class_ids=list(stats["class_ids"]),
            )

            if not self.channels:
                print(f"INFO: {summary.total_alerts} alerta(s) na janela, mas nenhum canal de notificação configurado.")

            for channel in self.channels:
                try:
                    await channel.send(summary)
                    print(f"INFO: Notificação enviada via {channel.__class__.__name__}.")
                except Exception as e:
                    print(f"ERRO: Falha ao notificar via {channel.__class__.__name__}: {e}")
