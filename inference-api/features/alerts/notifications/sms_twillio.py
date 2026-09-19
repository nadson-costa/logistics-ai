import twillio

from .schemas import AlertSummary

class TwillioSMSChannel:
    def __init__(self, account_sid: str, auth_token: str, sender: str, recipient: str):
        self.client = twillio.Client(account_sid, auth_token)
        self._from = sender
        self._to = recipient

    async def send(self, summary: AlertSummary) -> None:
        classes = ", ".join(str(class_id) for class_id in summary.class_ids)

        message_body = (
            f"Alerta de baixa confiança — YOLOv11-Logistics-Box\n"
            f"Período: {summary.window_start:%d/%m %H:%M:%S} — {summary.window_end:%d/%m %H:%M:%S}\n"
            f"Total de alertas: {summary.total_alerts}\n"
            f"Confiança média: {summary.avg_confidence:.3f}\n"
            f"Confiança mínima: {summary.min_confidence:.3f}\n"
            f"Classes envolvidas: {classes}"
        )

        await self.client.messages.create_async(
            body=message_body,
            from_=self._from,
            to=self._to
        )