import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async def init_db():
    conn = await asyncpg.connect(DB_URL)
    try:
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
        print("INFO: Tabela 'detection_alerts' verificada/criada com sucesso via .env.")
    finally:
        await conn.close()