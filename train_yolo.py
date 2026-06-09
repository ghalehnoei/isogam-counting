#!/usr/bin/env python3
"""
YOLO Training Script for Isogam Counting
Trains an object detection model using Ultralytics YOLO
"""

import os
import yaml
from pathlib import Path
from ultralytics import YOLO


def create_dataset_structure():
    """Create the standard dataset structure if it doesn't exist"""
    dirs = [
        'dataset/images/train',
        'dataset/images/val',
        'dataset/labels/train',
        'dataset/labels/val',
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("Dataset structure created.")


def create_data_yaml():
    """Create data.yaml configuration file"""
    data = {
        'path': 'dataset',  # dataset root path
        'train': 'images/train',
        'val': 'images/val',
        'nc': 1,  # number of classes (adjust if you have multiple)
        'names': ['isogam']  # class names (adjust as needed)
    }
    
    with open('data.yaml', 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print("data.yaml created.")


def train_yolo_model():
    """Train YOLO model"""
    
    # Load a pretrained model (y8n = nano, y6s = small, etc.)
    # Options: y11n, y10n, y8n, y6n, y3n, y5n, y4n, y2n, y1x, y8, y6, y5, y3
    model = YOLO('yolov8n.pt')  # starts with pretrained weights
    
    # Train the model
    results = model.train(
        data='data.yaml',         # path to data.yaml
        epochs=100,               # number of training epochs
        imgsz=640,                # image size
        batch=16,                 # batch size (adjust based on GPU memory)
        name='isogam_detection',  # experiment name
        project='runs/detect',    # project name
        patience=20,              # early stopping patience
        lr0=0.01,                 # initial learning rate
        weight_decay=0.0005,      # weight decay
        momentum=0.937,           # momentum
        cos_lr=True,              # cosine learning rate scheduler
        close_mosaic=10,          # disable mosaic augmentation for final epochs
        amp=True,                 # automatic mixed precision training
        device=0,                 # GPU device (0 = first GPU, cpu = CPU)
        workers=8,                # data loading workers
        cache=False,              # cache images (--disk to disk cache)
        augment=True,             # auto augmentation
        save=True,                # save train checkpoints and results
        save_period=10,           # save checkpoint every N epochs
        val=True,                 # validate at the end of each epoch
        plots=True,               # save plots and confusion matrix
        verbose=True,             # print verbose output
    )
    
    return results


def export_model(model_format='onnx'):
    """Export trained model to different formats"""
    model = YOLO('runs/detect/isogam_detection/weights/best.pt')
    
    formats = {
        'onnx': 'yolov8.onnx',
        'torchscript': 'yolov8.torchscript.pt',
        'coreml': 'yolov8.mlmodel',
        'engine': 'yolov8.engine',
        'trt': 'yolov8.trt',
    }
    
    for fmt, filename in formats.items():
        if fmt == model_format:
            export_path = model.export(format=fmt)
            print(f"Model exported to {export_path}")


def validate_model():
    """Validate the trained model"""
    model = YOLO('runs/detect/isogam_detection/weights/best.pt')
    
    metrics = model.val()
    print(f"\nValidation Metrics:")
    print(f"  mAP@50: {metrics.box.map50:.4f}")
    print(f"  mAP@50-95: {metrics.box.map:.4f}")
    print(f"  Precision: {metrics.box.mp:.4f}")
    print(f"  Recall: {metrics.box.mr:.4f}")


def run_inference(image_path, confidence=0.5):
    """Run inference on a single image"""
    model = YOLO('runs/detect/isogam_detection/weights/best.pt')
    
    results = model.predict(
        source=image_path,
        conf=confidence,
        iou=0.45,
        agnostic_nms=False,
        show=False,
        save=True,
        save_txt=True,
        save_conf=True,
        save_crop=False,
    )
    
    return results


if __name__ == '__main__':
    print("=" * 60)
    print("YOLO Isogam Counting Training Script")
    print("=" * 60)
    
    # Step 1: Setup (uncomment if needed)
    # create_dataset_structure()
    # create_data_yaml()
    
    # Step 2: Train
    print("\n[INFO] Starting YOLO training...")
    results = train_yolo_model()
    
    print("\n[SUCCESS] Training completed!")
    print(f"Results saved to: runs/detect/isogam_detection/")
    
    # Step 3: Validate (uncomment if needed)
    # validate_model()
    
    # Step 4: Run inference (uncomment if needed)
    # results = run_inference('path/to/test/image.jpg')
    # for result in results:
    #     boxes = result.boxes
    #     print(f"Detected {len(boxes)} isogams")
