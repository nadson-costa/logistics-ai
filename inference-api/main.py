import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from core.database import create_pool, init_db
from features.alerts.notifications.dispatcher import NotificationDispatcher
from features.alerts.notifications.email_resend import ResendEmailChannel
from features.alerts.notifications.sms_twilio import TwilioSMSChannel
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

    notification_channels = []
    if settings.resend_api_key and settings.notification_email_to:
        notification_channels.append(
            ResendEmailChannel(
                api_key=settings.resend_api_key,
                sender=settings.notification_email_from,
                recipient=settings.notification_email_to,
            )
        )

    if settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_recipient:
        notification_channels.append(
            TwilioSMSChannel(
                account_sid=settings.twilio_account_sid,
                auth_token=settings.twilio_auth_token,
                sender=settings.twilio_sender,
                recipient=settings.twilio_recipient,
            )
        )

    dispatcher = NotificationDispatcher(
        repository=app.state.alert_repository,
        channels=notification_channels,
        window_seconds=settings.notification_window_seconds,
    )
    dispatcher_task = asyncio.create_task(dispatcher.run())

    print("INFO: Aplicação iniciada com sucesso.")
    yield

    worker_task.cancel()
    dispatcher_task.cancel()

    for channel in notification_channels:
        close = getattr(channel, "close", None)
        if close is not None:
            await close()

    await app.state.db_pool.close()


app = FastAPI(title="Logistics AI", version="0.1.0", lifespan=lifespan)

app.include_router(inspection_router)
app.include_router(alerts_router)