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

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
