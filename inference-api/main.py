import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.database import create_pool, init_db
from features.alerts.repository import AlertRepository
from features.alerts.router import router as alerts_router
from features.alerts.worker import AlertWorker
from features.inspection.router import router as inspection_router
from features.inspection.service import InspectionService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await create_pool()
    await init_db(app.state.db_pool)

    app.state.inspection_service = InspectionService()
    app.state.alert_repository = AlertRepository(app.state.db_pool)

    worker = AlertWorker(app.state.alert_repository)
    worker_task = asyncio.create_task(worker.consume_events())

    print("INFO: Aplicação iniciada com sucesso.")
    yield

    worker_task.cancel()
    await app.state.db_pool.close()


app = FastAPI(title="Logistics AI", version="0.1.0", lifespan=lifespan)

app.include_router(inspection_router)
app.include_router(alerts_router)