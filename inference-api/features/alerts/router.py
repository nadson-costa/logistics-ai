from typing import Optional

from fastapi import APIRouter, Depends, Query, Request

from .repository import AlertRepository
from .schemas import AlertListResponse, AlertOut

router = APIRouter(prefix="/api/v1/alerts", tags=["Alerts"])


def get_alert_repository(request: Request) -> AlertRepository:
    return request.app.state.alert_repository


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    class_id: Optional[int] = Query(None, description="Filtra por ID da classe detectada"),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0),
    max_confidence: Optional[float] = Query(None, ge=0.0, le=1.0),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    repository: AlertRepository = Depends(get_alert_repository),
):
    rows, total = await repository.list_alerts(
        class_id=class_id,
        min_confidence=min_confidence,
        max_confidence=max_confidence,
        limit=limit,
        offset=offset,
    )

    return AlertListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=[AlertOut(**dict(row)) for row in rows],
    )
