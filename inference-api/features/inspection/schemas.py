from pydantic import BaseModel, Field

class DetectionEvent(BaseModel):
    type: str = Field(default="LOW_CONFIDENCE_ALERT", description="Tipo de evento de detecção")
    frame_index: int = Field(..., description="O número do quadro no vídeo onde ocorreu a detecção")
    confidence: float = Field(..., description="O grau de confiança da IA (0.0 a 1.0)")
    class_id: int = Field(..., description="O ID da classe detectada")

class InspectionResponse(BaseModel):
    status: str
    message: str