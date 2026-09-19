from twilio.http.async_http_client import AsyncTwilioHttpClient
from twilio.rest import Client

from .schemas import AlertSummary


class TwilioSMSChannel:
    def __init__(self, account_sid: str, auth_token: str, sender: str, recipient: str):
        self.client = Client(account_sid, auth_token, http_client=AsyncTwilioHttpClient())
        self._from = sender
        self._to = recipient

    async def send(self, summary: AlertSummary) -> None:
        await self.client.messages.create_async(
            body="sms_internal_alerts",
            from_=self._from,
            to=self._to
        )

    async def close(self) -> None:
        await self.client.http_client.close()
