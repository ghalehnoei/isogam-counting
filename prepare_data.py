import os
import shutil
import yaml
from pathlib import Path
from sklearn.model_selection import train_test_split
from PIL import Image
import argparse


def prepare_yolo_dataset(
    source_dir,
    output_dir="data",
    train_ratio=0.8,
    val_ratio=0.1,
    test_ratio=0.1,
    class_names=None,
):
    """
    Prepare dataset for YOLO training.
    
    Expected source structure:
        source_dir/
            images/
                img1.jpg, img2.jpg, ...
            labels/
                img1.txt, img2.txt, ...  (YOLO format: class x_center y_center width height)
    
    Output structure:
        data/
            images/
                train/
                val/
                test/
            labels/
                train/
                val/
                test/
            data.yaml
    """
    
    source_dir = Path(source_dir)
    output_dir = Path(output_dir)
    
    # Create output directories
    for split in ["train", "val", "test"]:
        (output_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (output_dir / "labels" / split).mkdir(parents=True, exist_ok=True)
    
    # Get list of images and labels
    images_dir = source_dir / "images"
    labels_dir = source_dir / "labels"
    
    if not images_dir.exists():
        print(f"Error: {images_dir} not found!")
        return
    
    image_files = sorted([f for f in images_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']])
    
    if not image_files:
        print(f"No images found in {images_dir}")
        return
    
    print(f"Found {len(image_files)} images")
    
    # Split dataset
    train_size = int(len(image_files) * train_ratio)
    val_size = int(len(image_files) * val_ratio)
    
    train_files, remaining = train_test_split(
        image_files, test_size=1-train_ratio, random_state=42
    )
    val_files, test_files = train_test_split(
        remaining, test_size=test_ratio/(val_ratio+test_ratio), random_state=42
    )
    
    print(f"Train: {len(train_files)}, Val: {len(val_files)}, Test: {len(test_files)}")
    
    # Copy files to output directories
    for img_file in train_files:
        label_file = labels_dir / (img_file.stem + ".txt")
        shutil.copy2(img_file, output_dir / "images" / "train" / img_file.name)
        if label_file.exists():
            shutil.copy2(label_file, output_dir / "labels" / "train" / label_file.name)
    
    for img_file in val_files:
        label_file = labels_dir / (img_file.stem + ".txt")
        shutil.copy2(img_file, output_dir / "images" / "val" / img_file.name)
        if label_file.exists():
            shutil.copy2(label_file, output_dir / "labels" / "val" / label_file.name)
    
    for img_file in test_files:
        label_file = labels_dir / (img_file.stem + ".txt")
        shutil.copy2(img_file, output_dir / "images" / "test" / img_file.name)
        if label_file.exists():
            shutil.copy2(label_file, output_dir / "labels" / "test" / label_file.name)
    
    print(f"✓ Data copied to {output_dir}")
    
    # Auto-detect class names if not provided
    if class_names is None:
        class_names = detect_classes(output_dir / "labels" / "train")
    
    # Create data.yaml
    data_yaml = {
        "path": str(output_dir.absolute()),
        "train": str((output_dir / "images" / "train").absolute()),
        "val": str((output_dir / "images" / "val").absolute()),
        "test": str((output_dir / "images" / "test").absolute()),
        "nc": len(class_names),
        "names": class_names,
    }
    
    yaml_path = output_dir / "data.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(data_yaml, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Created {yaml_path}")
    print(f"✓ Classes: {class_names}")
    
    return yaml_path


def detect_classes(labels_dir):
    """Auto-detect class indices from label files."""
    classes = set()
    
    for label_file in Path(labels_dir).glob("*.txt"):
        with open(label_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    class_id = int(parts[0])
                    classes.add(class_id)
    
    max_class = max(classes) if classes else 0
    return {i: f"class_{i}" for i in range(max_class + 1)}


def main():
    parser = argparse.ArgumentParser(description="Prepare dataset for YOLO training")
    parser.add_argument("--source", type=str, default="dataset", help="Source dataset directory")
    parser.add_argument("--output", type=str, default="data", help="Output directory")
    parser.add_argument("--train", type=float, default=0.7, help="Training set ratio")
    parser.add_argument("--val", type=float, default=0.15, help="Validation set ratio")
    parser.add_argument("--test", type=float, default=0.15, help="Test set ratio")
    parser.add_argument("--classes", type=str, help="Comma-separated class names (e.g., 'person,car,dog')")
    
    args = parser.parse_args()
    
    class_names = None
    if args.classes:
        class_names = args.classes.split(",")
    
    prepare_yolo_dataset(
        source_dir=args.source,
        output_dir=args.output,
        train_ratio=args.train,
        val_ratio=args.val,
        test_ratio=args.test,
        class_names=class_names,
    )


if __name__ == "__main__":
    main()
