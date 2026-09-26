import cv2
import os

def extract_frames(video_path, output_dir, frame_interval=None):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"ERRO: Não foi possível abrir o vídeo {video_path}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"Vídeo carregado com sucesso. taxa de quadros: {fps} fps")

    if frame_interval is None:
        frame_interval = fps

    frame_count = 0
    save_count = 0

    print("Iniciando extração...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            filename = f"frame_{frame_count:04d}.jpg"
            output_path = os.path.join(output_dir, filename)

            cv2.imwrite(output_path, frame)
            save_count += 1

        frame_count += 1

    cap.release()
    print(f"OK: Extração concluída! {save_count} frames salvos em '{output_dir}'")

if __name__ == "__main__":
    video_path = "data/raw/esteira.mp4"
    output_dir = "data/frames"
    extract_frames(video_path, output_dir)