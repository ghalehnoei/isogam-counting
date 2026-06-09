"""
Helper to generate train/val split directories from your raw images + labels.

Usage:
    python make_splits.py --images_dir /path/to/images --out data --train_pct 0.9 --classes isogam --type pose
"""

import argparse
import os
import shutil
import random


def main():
    parser = argparse.ArgumentParser(description="Split dataset into train/val folders")
    parser.add_argument("--images_dir", required=True, help="Folder with all images (jpg/png) and annotations")
    parser.add_argument("--out", default="data", help="Output directory structure")
    parser.add_argument("--train_pct", type=float, default=0.9, help="Training split percentage")
    parser.add_argument("--classes", nargs="+", default=["isogam"], help="Class names (for pose: list landmark names)")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    # Collect image files
    supported_ext = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    all_images = []
    for f in sorted(os.listdir(args.images_dir)):
        if os.path.splitext(f)[1].lower() in supported_ext:
            all_images.append(f)

    if not all_images:
        print("No images found. Nothing to do.")
        return

    random.shuffle(all_images)
    split = int(len(all_images) * args.train_pct)
    train_set, val_set = all_images[:split], all_images[split:]

    print(f"Images : {len(all_images)}")
    print(f"Train  : {len(train_set)} | Val  : {len(val_set)}")

    # Build output structure:
    #   data/
    #     train/
    #       images/ ...jpg
    #       labels/ ...txt (YOLO format)
    #     val/
    #       images/ ...jpg
    #       labels/ ...txt
    for split_name in ("train", "val"):
        base = args.out / split_name if isinstance(args.out, str) else split_name
        for subdir in ["images", "labels"]:
            os.makedirs(os.path.join(base, subdir), exist_ok=True)

    def _copy_set(file_list, set_name):
        for fname in file_list:
            stem = os.path.splitext(fname)[0]
            src_image = os.path.join(args.images_dir, fname)
            dst_img = getattr(args.out, set_name, "images") / fname  # noqa: F821

    shutil.copy(src_image, str(dst_img))

    # Copy annotation files (same stem as image)
        for fname in file_list:
            stem = os.path.splitext(fname)[0]
            ann_src = None
            for ext in (".txt", ".json", ".xml"):
                candidate = f"{stem}{ext}"
                if os.path.exists(os.path.join(args.images_dir, candidate)):
                    ann_src = os.path.join(args.images_dir, candidate)
                    break
            if ann_src:
                dst_ann = os.path.join(base / "labels" , f"{stem}.txt")
                shutil.copy(ann_src, dst_ann)

    _copy_set(train_set, "train")
    _copy_set(val_set, "val")

    print(f"\nDone. Output at {args.out}/")
    print("Next: create data.yaml (see template below)")


if __name__ == "__main__":
    main()
