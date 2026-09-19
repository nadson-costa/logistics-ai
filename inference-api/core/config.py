import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5005")
    mlflow_experiment_name: str = "logistics-model-health"
    mlflow_model_name: str = "YOLOv11-Logistics-Box"

    video_source_path: str = os.getenv("VIDEO_SOURCE_PATH", "data/raw/esteira.mp4")
    frame_sample_rate: int = int(os.getenv("FRAME_SAMPLE_RATE", "10"))
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))

    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_port: str = os.getenv("POSTGRES_PORT")
    postgres_db: str = os.getenv("POSTGRES_DB")

    notification_window_seconds: int = int(os.getenv("NOTIFICATION_WINDOW_SECONDS", "300"))

    resend_api_key: str = os.getenv("RESEND_API_KEY", "")
    notification_email_from: str = os.getenv("NOTIFICATION_EMAIL_FROM", "logistics-ai@nadson.dev")
    notification_email_to: str = os.getenv("NOTIFICATION_EMAIL_TO", "")

    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_sender: str = os.getenv("TWILIO_SENDER", "")
    twilio_recipient: str = os.getenv("TWILIO_RECIPIENT", "")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
