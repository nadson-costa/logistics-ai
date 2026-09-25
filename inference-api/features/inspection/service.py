import cv2
import asyncio
import mlflow
import os
import threading
import time
from typing import Optional
from ultralytics import YOLO
from core.config import settings
from .schemas import DetectionEvent

mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

def get_production_model():
    model_name = settings.mlflow_model_name
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
        self._defect_class_id = self._resolve_defect_class_id()

        self._latest_frame: Optional[bytes] = None
        self._latest_frame_lock = threading.Lock()

    def _resolve_defect_class_id(self) -> Optional[int]:
        for class_id, name in self.model.names.items():
            if name == settings.defect_class_name:
                return class_id
        print(f"AVISO: Classe '{settings.defect_class_name}' não existe no modelo carregado — alertas de defeito desativados.")
        return None

    def get_latest_frame(self) -> Optional[bytes]:
        with self._latest_frame_lock:
            return self._latest_frame

    def _set_latest_frame(self, frame_bytes: bytes) -> None:
        with self._latest_frame_lock:
            self._latest_frame = frame_bytes

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

                if frame_count % settings.frame_sample_rate == 0:
                    results = self.model.predict(frame, imgsz=640, verbose=False)

                    annotated_frame = results[0].plot()
                    ok, encoded = cv2.imencode(".jpg", annotated_frame)
                    if ok:
                        self._set_latest_frame(encoded.tobytes())

                    for box in results[0].boxes:
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])

                        if class_id == self._defect_class_id:
                            detection_event = DetectionEvent(
                                type="DEFECT_DETECTED",
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