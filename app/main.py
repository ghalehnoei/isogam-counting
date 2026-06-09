import base64
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.counter import PoseCounter

MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

app = FastAPI(title="Isogam Counter")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

_models: dict[str, PoseCounter] = {}


def _get_model(model_name: str) -> PoseCounter:
    if model_name not in _models:
        model_path = MODEL_DIR / model_name
        if not model_path.exists():
            raise ValueError(f"Model '{model_name}' not found")
        _models[model_name] = PoseCounter(str(model_path))
    return _models[model_name]


@app.get("/", response_class=HTMLResponse)
async def index():
    html = (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.get("/models/")
async def list_models():
    models = sorted(f.name for f in MODEL_DIR.glob("*.pt"))
    return {"models": models}


def _img_to_b64(image: np.ndarray) -> str:
    _, buffer = cv2.imencode(".jpg", image)
    return base64.b64encode(buffer).decode("utf-8")


@app.post("/predict/")
async def predict(file: UploadFile = File(...), conf: float = Form(0.5), iou: float = Form(0.7), model_name: str = Form("isogam-pose.pt"), imgsz: int = Form(0)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        return JSONResponse({"error": "Could not decode image"}, status_code=400)

    counter = _get_model(model_name)
    kw = dict(conf=conf, iou=iou)
    if imgsz:
        kw["imgsz"] = imgsz
    result = counter.count(image, **kw)
    annotated_bbox = counter.draw_annotations(image, **kw)
    annotated_circle = counter.draw_circle_annotations(image, **kw)

    return JSONResponse({
        "count": result["count"],
        "dedup_count": result["dedup_count"],
        "detections": result["detections"],
        "original_b64": _img_to_b64(image),
        "bbox_b64": _img_to_b64(annotated_bbox),
        "circle_b64": _img_to_b64(annotated_circle),
    })
