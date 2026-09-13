import asyncio
from fastapi import FastAPI
from core.database import init_db
from features.inspection.router import router as inspection_router
from features.alerts.worker import AlertWorker
from features.alerts.repository import AlertRepository

app = FastAPI(title="Logistics AI", version="0.1.0")

app.include_router(inspection_router)

@app.on_event("startup")
async def startup_event():
    await init_db()  

    repository = AlertRepository()
    worker = AlertWorker(repository)
    
    asyncio.create_task(worker.consume_events())
    print("INFO: Aplicação iniciada com sucesso.")