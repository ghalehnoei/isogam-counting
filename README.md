# Isogam Counter

A web app for counting objects in images and videos using YOLO models (pose and detection) with ByteTracker-based tracking.

## Features

- **Image** upload support
- **Multi-model**: works with both YOLO pose and YOLO detection models
- **Duplicate detection** highlights very close centers in a different color
- **Manual trigger**: press <kbd>Enter</kbd> (or click "Detect") to run detection
- **Comparison slider** to compare original vs detected frame
- **Adjustable confidence** threshold
- **Adjustable IoU** threshold for overlap detection
- **Dark glassmorphism** UI

## Project structure

```
Isogam-Counting/
├── app/
│   ├── __init__.py
│   ├── counter.py     # YOLO + ByteTracker logic
│   └── main.py        # FastAPI server
├── templates/
│   └── index.html     # Web UI
├── models/            # YOLO model files (.pt)
├── static/            # Static assets
└── .venv/             # Python virtual environment
```

## Requirements

- Python 3.10+
- Windows / macOS / Linux
- The `.venv/` in this repo already has the dependencies installed. If you set up a new environment, you will need:

```
ultralytics
opencv-python
numpy
fastapi
uvicorn
python-multipart
```

## Running

The repo ships with a virtual environment. Use it directly:

### Windows (PowerShell)

```powershell
& ".\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Windows (CMD)

```cmd
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### macOS / Linux

```bash
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then open <http://127.0.0.1:8000> in your browser.

If you need to reload on code changes, add `--reload`.

## Models

Place your trained YOLO `.pt` files inside the `models/` directory. They will appear in the **Model** dropdown in the UI. The app auto-detects whether a model is a pose or detection model from its `task` field.

Detection models are inferred at `imgsz=1920` for better small-object recall. Pose models use the default size.

## API

### `GET /models/`

Returns the list of available models.

```json
{ "models": ["isogam-pose.pt", "best-Ali.pt"] }
```

### `POST /predict/`

Runs detection on a single image.

Form fields:

- `file`: image file
- `conf`: confidence threshold (0-1)
- `iou`: IoU threshold (0-1)
- `model_name`: filename inside `models/`

Response: JSON with `count`, `dedup_count`, `detections`, `original_b64`, `annotated_b64`.

## Counters

- **Raw**: number of detections in the image
- **Deduplicated**: detections with very close centers collapsed
