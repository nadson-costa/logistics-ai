import resend

from .schemas import AlertSummary


class ResendEmailChannel:
    def __init__(self, api_key: str, sender: str, recipient: str):
        resend.api_key = api_key
        self._from = sender
        self._to = recipient

    async def send(self, summary: AlertSummary) -> None:
        classes = ", ".join(str(class_id) for class_id in summary.class_ids)

        html = f"""
            <h2>Defeitos detectados — YOLOv11-Logistics-Box</h2>
            <p>Período: {summary.window_start:%d/%m %H:%M:%S} — {summary.window_end:%d/%m %H:%M:%S}</p>
            <ul>
                <li>Total de defeitos: {summary.total_alerts}</li>
                <li>Confiança média: {summary.avg_confidence:.3f}</li>
                <li>Confiança mínima: {summary.min_confidence:.3f}</li>
                <li>Classes envolvidas: {classes}</li>
            </ul>
        """

        await resend.Emails.send_async({
            "from": self._from,
            "to": [self._to],
            "subject": f"[Logistics AI] {summary.total_alerts} defeitos detectados",
            "html": html,
        })
