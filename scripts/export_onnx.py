from ultralytics import YOLO

def export_model():
    print("INFO: Carregando os pesos do modelo treinado")

    model_path = "/opt/homebrew/runs/detect/mlruns/detector_caixas_v1-11/weights/best.pt"
    model = YOLO(model_path)

    print("INFO: Convertendo a arquitetura para o formato ONNX")
    model.export(format="onnx", imgsz=640)

    print("Conversão finalizada! O arquivo .onnx foi salvo na mesma pasta do modelo treinado.")

if __name__ == "__main__":
    export_model()