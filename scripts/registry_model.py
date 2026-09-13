import mlflow
import mlflow.onnx
import onnx

mlflow.set_tracking_uri("http://127.0.0.1:5005")

EXPERIMENT_NAME = "logistics-cv-pipeline"
MODEL_NAME = "YOLOv11-Logistics-Box"

mlflow.set_experiment(EXPERIMENT_NAME)

print("INFO: Iniciando registro do modelo no MLflow...")

with mlflow.start_run() as run:
    model_path = "inference-api/model/best.onnx"
    onnx_model = onnx.load(model_path)

    mlflow.onnx.log_model(
        onnx_model=onnx_model,
        artifact_path="model"
    )

    model_uri = f"runs:/{run.info.run_id}/model"
    mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)

    print(f"OK: Modelo registrado com sucesso no MLflow! Run ID: {run.info.run_id}")