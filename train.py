from ultralytics import YOLO
import sys
import os


def main():
    # --- Edit these to match your setup ---
    task = "detect"          # "pose" or "detect"
    model_size = "11l"       # Model size: 11n, 11s, 11m, 11l, 11x, 26s, 26l, etc.
    data_yaml = "./data/data.yaml"  # path to dataset YAML (relative or absolute)
    epochs = 200
    imgsz = 1280
    batch_size = 2
    device = 0               # 0 for GPU, "cpu" or -1 for CPU
    project_name = "runs/train"
    name = "isogam"          # folder name under runs/
    pretrained = True        # False to train from scratch
    cache = "disk"           # "ram", "disk", or "" (no cache)
    workers = 8              # dataloader workers
    patience = 30            # early stopping patience
    save_period = 10         # checkpoint every N epochs
    amp = False               # mixed precision
    optimizer = "AdamW"      # auto, SGD, Adam, AdamW
    close_mosaic = 10        # disable mosaic augmentation last N epochs
    resume_last = False      # if True and output folder exists, resume from last checkpoint
    
    # Learning rate and weight decay
    lr0 = 0.0005
    weight_decay = 0.0005
    cos_lr = True
    
    # Augmentation parameters
    hsv_h = 0.01
    hsv_s = 0.3
    hsv_v = 0.2
    degrees = 15
    translate = 0.05
    scale = 0.2
    fliplr = 0.5
    mosaic = 0.0
    mixup = 0.0
    # --- End of config ---

    task_lower = task.lower()
    if task_lower not in ("pose", "detect"):
        print(f"Unsupported task: {task}. Choose 'pose' or 'detect'.")
        sys.exit(1)

    # Automatically set model name based on task
    if task_lower == "pose":
        model_name = f"yolo{model_size}-pose"
    else:
        model_name = f"yolo{model_size}"

    model_path = None
    if pretrained:
        model_path = f"{model_name}.pt"
    else:
        model_path = f"yolo11n-{task_lower}.pt"  # base weights for ultralytics

    print(f"Task      : {task}")
    print(f"Base model: {model_name} ({model_path})")
    print(f"Data YAML : {data_yaml}")
    print(f"Epochs    : {epochs}")
    print(f"Imgsz     : {imgsz}")
    print(f"Batch     : {batch_size}")
    print(f"Device    : {device}")
    print(f"Project   : {project_name}/{name}")
    if resume_last:
        print("Resume on:  True")
    else:
        print("Resume on: False")

    # Load model
    model = YOLO(model_path)

    # Train
    results = model.train(
        task=task,
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch_size,
        device=device,
        project=project_name,
        name=name,
        cache=cache,
        workers=workers,
        patience=patience,
        save_period=save_period,
        val=True,
        amp=amp,
        optimizer=optimizer,
        close_mosaic=close_mosaic,
        lr0=lr0,
        weight_decay=weight_decay,
        cos_lr=cos_lr,
        hsv_h=hsv_h,
        hsv_s=hsv_s,
        hsv_v=hsv_v,
        degrees=degrees,
        translate=translate,
        scale=scale,
        fliplr=fliplr,
        mosaic=mosaic,
        mixup=mixup,
        verbose=True,
    )

    print("\nTraining complete! Best model saved at:")
    best_path = os.path.join(project_name, name, "weights", "best.pt")
    print(best_path)


if __name__ == "__main__":
    main()
