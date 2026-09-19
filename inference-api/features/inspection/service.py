import cv2
import asyncio
import mlflow
import os
import time
from ultralytics import YOLO
from .schemas import DetectionEvent

MLFLOW_URL = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5005")
mlflow.set_tracking_uri(MLFLOW_URL)

def get_production_model():
    model_name = "YOLOv11-Logistics-Box"
    print(f"INFO: Conectando ao MLflow e buscando a última versão do {model_name}...")
    try:
        model_uri = f"models:/{model_name}/latest"
        artifact_path = mlflow.artifacts.download_artifacts(artifact_uri=model_uri)
        onnx_file_path = os.path.join(artifact_path, "model.onnx")
        
        print(f"OK: Modelo baixado para cache em {onnx_file_path}")
        return onnx_file_path
    except Exception as e:
        print(f"ERRO: Falha ao conectar no MLflow: {e}")
        return "inference-api/model/best.onnx"

class InspectionService:
    def __init__(self, model_path: str = None):
        if model_path is None:
            model_path = get_production_model()
            
        print(f"INFO: Carregando modelo de {model_path}")
        self.model = YOLO(model_path, task="detect")

    async def process_video_stream(self, video_path: str, event_queue: asyncio.Queue):
        loop = asyncio.get_running_loop()
        await asyncio.to_thread(self._process_video_sync, video_path, event_queue, loop)

    def _process_video_sync(self, video_path: str, event_queue: asyncio.Queue, loop: asyncio.AbstractEventLoop):
        print(f"INFO: Conectando em {video_path}")
        cap = cv2.VideoCapture(video_path)

        try:
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
                            loop.call_soon_threadsafe(event_queue.put_nowait, detection_event)

                frame_count += 1
                time.sleep(0.01)
        except Exception as e:
            print(f"ERRO: Falha ao processar o vídeo: {e}")
        finally:
            cap.release()