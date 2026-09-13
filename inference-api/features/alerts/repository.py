import asyncpg
from core.database import DB_URL
from features.inspection.schemas import DetectionEvent

class AlertRepository:
    async def save_alert(self, event: DetectionEvent):
        conn = await asyncpg.connect(DB_URL)
        try:
            await conn.execute('''
                INSERT INTO detection_alerts (event_type, frame_index, confidence, class_id)
                VALUES ($1, $2, $3, $4)
            ''',
                event.type, event.frame_index, event.confidence, event.class_id
            )
            print(f"INFO: Salvando alerta no PostgreSQL: Frame {event.frame_index} | Confiança {event.confidence} | Classe {event.class_id}")
        finally:
            await conn.close()