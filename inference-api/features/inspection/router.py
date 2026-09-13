import asyncio
from fastapi import APIRouter, BackgroundTasks, Depends
from .schemas import InspectionResponse
from .service import InspectionService
from core.events import get_queue

router = APIRouter(prefix="/api/v1/inspection", tags=["Inspection"])

inspection_service_singleton = InspectionService()

def get_inspection_service() -> InspectionService:
    return inspection_service_singleton

@router.post("/start", response_model=InspectionResponse)
async def start_inspection(
    background_tasks: BackgroundTasks,
    service: InspectionService = Depends(get_inspection_service),
    event_queue: asyncio.Queue = Depends(get_queue)
):
    video_source = "data/raw/esteira.mp4"
    
    background_tasks.add_task(service.process_video_stream, video_source, event_queue)
    
    return InspectionResponse(
        status="success",
        message="Video stream processing started in the background."
    )