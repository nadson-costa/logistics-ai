from ultralytics import YOLO

def train_model():
    print("INFO: Iniciando o treinamento do modelo")

    model = YOLO("yolov8n.pt")

    results = model.train(
        data = "data/dataset_yolo/data.yaml",
        epochs = 50,
        imgsz = 640,
        device = "mps",
        batch = 8,
        project = "mlruns",
        name = "detector_caixas_v1"
    )

    print("OK: Treinamento concluído com sucesso!")

if __name__ == "__main__":
    train_model()
