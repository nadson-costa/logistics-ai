import mlflow
import asyncio
from core.config import settings
from core.events import detection_queue
from .repository import AlertRepository

class AlertWorker:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    def send_alert(self, event):
        try:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            mlflow.set_experiment(settings.mlflow_experiment_name)

            with mlflow.start_run(run_name=f"alert_frame_{event.frame_index}"):
                mlflow.log_metric("confidence_score", event.confidence)
                mlflow.log_param("class_id", event.class_id)

            print(f"TRACKING: Defeito registrado no MLflow! (Confiança: {event.confidence})")

        except Exception as e:
            print(f"ERRO: Falha ao enviar métrica para o MLflow: {e}")

    async def consume_events(self):
        print("INFO: Worker comecou a ouvir eventos de detecção...")
        while True:
            event = await detection_queue.get()
            print(f"INFO: Worker recebeu o evento: {event.type}")
            
            await self.repository.save_alert(event)

            if event.type == "DEFECT_DETECTED":
                asyncio.create_task(asyncio.to_thread(self.send_alert, event))
            
            detection_queue.task_done()