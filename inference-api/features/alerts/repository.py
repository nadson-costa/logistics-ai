import asyncpg
from features.inspection.schemas import DetectionEvent

class AlertRepository:
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def save_alert(self, event: DetectionEvent):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO detection_alerts (event_type, frame_index, confidence, class_id)
                VALUES ($1, $2, $3, $4)
            ''',
                event.type, event.frame_index, event.confidence, event.class_id
            )
        print(f"INFO: Salvando alerta no PostgreSQL: Frame {event.frame_index} | Confiança {event.confidence} | Classe {event.class_id}")