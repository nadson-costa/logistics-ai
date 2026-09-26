import asyncio
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.responses import StreamingResponse
from .schemas import InspectionResponse
from .service import InspectionService
from core.config import settings
from core.events import get_queue

router = APIRouter(prefix="/api/v1/inspection", tags=["Inspection"])

STREAM_INTERVAL_SECONDS = 0.1

def get_inspection_service(request: Request) -> InspectionService:
    return request.app.state.inspection_service

@router.post("/start", response_model=InspectionResponse)
async def start_inspection(
    background_tasks: BackgroundTasks,
    service: InspectionService = Depends(get_inspection_service),
    event_queue: asyncio.Queue = Depends(get_queue)
):
    background_tasks.add_task(service.process_video_stream, settings.video_source_path, event_queue)

    return InspectionResponse(
        status="success",
        message="Video stream processing started in the background."
    )

async def _frame_generator(service: InspectionService):
    while True:
        frame = service.get_latest_frame()
        if frame is not None:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
        await asyncio.sleep(STREAM_INTERVAL_SECONDS)

@router.get("/stream")
async def stream_inspection(service: InspectionService = Depends(get_inspection_service)):
    return StreamingResponse(
        _frame_generator(service),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )