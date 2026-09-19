from typing import Optional

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

    async def list_alerts(
        self,
        class_id: Optional[int] = None,
        min_confidence: Optional[float] = None,
        max_confidence: Optional[float] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[asyncpg.Record], int]:
        conditions = []
        params: list = []

        if class_id is not None:
            params.append(class_id)
            conditions.append(f"class_id = ${len(params)}")

        if min_confidence is not None:
            params.append(min_confidence)
            conditions.append(f"confidence >= ${len(params)}")

        if max_confidence is not None:
            params.append(max_confidence)
            conditions.append(f"confidence <= ${len(params)}")

        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        async with self.pool.acquire() as conn:
            total = await conn.fetchval(
                f"SELECT COUNT(*) FROM detection_alerts {where_clause}", *params
            )

            rows = await conn.fetch(
                f'''
                    SELECT id, event_type, frame_index, confidence, class_id, created_at
                    FROM detection_alerts
                    {where_clause}
                    ORDER BY created_at DESC
                    LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
                ''',
                *params, limit, offset,
            )

        return list(rows), total