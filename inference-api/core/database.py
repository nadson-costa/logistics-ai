import asyncpg
from core.config import settings


async def create_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(settings.database_url)


async def init_db(pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS detection_alerts (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50),
                frame_index INTEGER,
                confidence REAL,
                class_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("INFO: Tabela 'detection_alerts' verificada/criada com sucesso.")