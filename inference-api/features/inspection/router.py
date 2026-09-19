import asyncio
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from .schemas import InspectionResponse
from .service import InspectionService
from core.config import settings
from core.events import get_queue

router = APIRouter(prefix="/api/v1/inspection", tags=["Inspection"])

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