import cv2
import asyncio
from ultralytics import YOLO
from .schemas import DetectionEvent

class InspectionService:
    def __init__(self, model_path: str = "inference-api/model/best.onnx"):
        print(f"INFO: Carregando modelo de {model_path}")
        self.model = YOLO(model_path, task="detect")

    async def process_video_stream(self, video_path: str, event_queue: asyncio.Queue):
        print(f"INFO: Conectando em {video_path}")
        cap = cv2.VideoCapture(video_path)

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("INFO: Fim do vídeo ou erro na leitura do quadro.")
                break

            if frame_count % 10 == 0:
                results = self.model.predict(frame, imgsz=640, verbose=False)

                for box in results[0].boxes:
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])

                    if confidence < 0.60:
                        detection_event = DetectionEvent(
                            type="LOW_CONFIDENCE_ALERT",
                            frame_index=frame_count,
                            confidence=round(confidence, 3),
                            class_id=class_id
                        )
                        await event_queue.put(detection_event)

            frame_count += 1
            await asyncio.sleep(0.01)

        cap.release()