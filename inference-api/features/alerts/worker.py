import mlflow
import asyncio
from core.events import detection_queue
from .repository import AlertRepository

mlflow.set_tracking_uri("http://127.0.0.1:5005")

class AlertWorker:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def consume_events(self):
        print("INFO: Worker comecou a ouvir eventos de detecção...")
        while True:
            event = await detection_queue.get()
            print(f"INFO: Worker recebeu o evento: {event.type}")
            
            await self.repository.save_alert(event)

            if event.type == "LOW_CONFIDENCE_ALERT":
                try:
                    mlflow.set_experiment("logistics-model-health")
                    
                    with mlflow.start_run(run_name=f"alert_frame_{event.frame_index}"):
                        mlflow.log_metric("confidence_score", event.confidence)
                        mlflow.log_param("class_id", event.class_id)
                        
                    print(f"TRACKING: Alerta de Drift registrado no MLflow! (Confiança: {event.confidence})")
                except Exception as e:
                    print(f"ERRO: Falha ao enviar métrica para o MLflow: {e}")
            
            detection_queue.task_done()