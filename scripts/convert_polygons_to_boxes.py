import glob


def polygon_to_box(class_id, coords):
    xs = coords[0::2]
    ys = coords[1::2]

    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    width = x_max - x_min
    height = y_max - y_min

    return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"


def convert_file(path):
    with open(path) as f:
        lines = [l.strip().split() for l in f if l.strip()]

    converted = False
    out_lines = []
    for parts in lines:
        class_id = parts[0]
        values = [float(v) for v in parts[1:]]

        if len(parts) == 5:
            out_lines.append(" ".join(parts))
        else:
            coords = values
            out_lines.append(polygon_to_box(class_id, coords))
            converted = True

    if converted:
        with open(path, "w") as f:
            f.write("\n".join(out_lines) + "\n")

    return converted


def main():
    label_files = glob.glob("data/dataset_yolo/train/labels/*.txt") + \
                  glob.glob("data/dataset_yolo/val/labels/*.txt")

    converted_count = 0
    for path in label_files:
        if convert_file(path):
            converted_count += 1

    print(f"OK: {converted_count} arquivos convertidos de polígono para box, de {len(label_files)} total.")


if __name__ == "__main__":
    main()
