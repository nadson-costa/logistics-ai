import asyncio
from core.events import detection_queue
from .repository import AlertRepository

class AlertWorker:
    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def consume_events(self):
        print("INFO: Worker comecou a ouvir eventos de detecção...")
        while True:
            event = await detection_queue.get()
            print(f"INFO: Worker recebeu o evento: {event.type}")
            
            await self.repository.save_alert(event)
            
            detection_queue.task_done()