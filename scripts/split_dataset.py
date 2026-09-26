import random
import shutil
from pathlib import Path

RANDOM_SEED = 42
VAL_RATIO = 0.2

DATASET_DIR = Path("data/dataset_yolo")
TRAIN_IMAGES = DATASET_DIR / "train" / "images"
TRAIN_LABELS = DATASET_DIR / "train" / "labels"
VAL_IMAGES = DATASET_DIR / "val" / "images"
VAL_LABELS = DATASET_DIR / "val" / "labels"


def split_dataset():
    VAL_IMAGES.mkdir(parents=True, exist_ok=True)
    VAL_LABELS.mkdir(parents=True, exist_ok=True)

    image_files = sorted(TRAIN_IMAGES.glob("*.jpg"))
    random.Random(RANDOM_SEED).shuffle(image_files)

    val_count = max(1, round(len(image_files) * VAL_RATIO))
    val_files = image_files[:val_count]

    for image_path in val_files:
        label_path = TRAIN_LABELS / f"{image_path.stem}.txt"

        shutil.move(str(image_path), str(VAL_IMAGES / image_path.name))
        if label_path.exists():
            shutil.move(str(label_path), str(VAL_LABELS / label_path.name))

    remaining = len(image_files) - len(val_files)
    print(f"OK: {len(val_files)} imagens movidas para validação, {remaining} permanecem em treino.")


if __name__ == "__main__":
    split_dataset()
