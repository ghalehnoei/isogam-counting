import cv2
import numpy as np
from ultralytics import YOLO


class PoseCounter:
    def __init__(self, model_path: str, conf_threshold: float = 0.5, iou_threshold: float = 0.7):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        self.names = self.model.names
        self.task = self.model.task
        self.is_pose = self.task == "pose"

    def _predict_kwargs(self, conf: float | None = None, iou: float | None = None, imgsz: int | None = None) -> dict:
        kwargs = {"conf": conf or self.conf_threshold, "verbose": False}
        if iou is not None:
            kwargs["iou"] = iou
        if imgsz is not None:
            kwargs["imgsz"] = imgsz
        return kwargs

    @staticmethod
    def _compute_iou(box_a: np.ndarray, box_b: np.ndarray) -> float:
        x1 = max(box_a[0], box_b[0])
        y1 = max(box_a[1], box_b[1])
        x2 = min(box_a[2], box_b[2])
        y2 = min(box_a[3], box_b[3])
        inter = max(0, x2 - x1) * max(0, y2 - y1)
        area_a = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
        area_b = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
        union = area_a + area_b - inter
        return inter / union if union > 0 else 0.0

    def _find_overlapping(self, boxes_xyxy: np.ndarray, iou_threshold: float) -> set[int]:
        overlapping = set()
        n = len(boxes_xyxy)
        for i in range(n):
            for j in range(i + 1, n):
                iou = self._compute_iou(boxes_xyxy[i], boxes_xyxy[j])
                if iou >= iou_threshold:
                    overlapping.add(j)
        return overlapping

    def count(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None):
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        result = results[0]
        boxes = result.boxes

        if boxes is None or len(boxes) == 0:
            return {"count": 0, "dedup_count": 0, "detections": []}

        boxes_np = boxes.xyxy.cpu().numpy()
        count = len(boxes_np)
        confs = boxes.conf.cpu().numpy().tolist()
        kpts_data = []
        if self.is_pose and result.keypoints is not None and result.keypoints.xy is not None:
            kpts_data = result.keypoints.xy.cpu().numpy().tolist()

        detections = []
        for i in range(count):
            detections.append({
                "bbox": boxes_np[i].tolist(),
                "confidence": round(confs[i], 3),
                "keypoints": kpts_data[i] if kpts_data else [],
            })

        overlapping = self._find_overlapping(boxes_np, iou_val)
        dedup_count = count - len(overlapping)

        return {
            "count": count,
            "dedup_count": max(0, dedup_count),
            "detections": detections,
        }

    def draw_annotations(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None):
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        return self._render_bbox_annotated(image, results[0], iou_val)

    def draw_circle_annotations(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None):
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        return self._render_circle_annotated(image, results[0], iou_val)

    def _render_bbox_annotated(self, frame: np.ndarray, result, iou_threshold: float) -> np.ndarray:
        annotated = frame.copy()
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            boxes_np = boxes.xyxy.cpu().numpy()
            overlapping = self._find_overlapping(boxes_np, iou_threshold)
            for i, box in enumerate(boxes_np):
                x1, y1, x2, y2 = box.astype(int)
                color = (0, 140, 255) if i in overlapping else (0, 0, 200)
                label = str(i + 1)
                bw, bh = x2 - x1, y2 - y1
                thickness = max(1, int(min(bw, bh) / 100))
                cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)
                font_scale = max(0.4, min(min(bw, bh) / 80, 1.2))
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness + 1)
                cv2.rectangle(annotated, (x1, y1 - th - 6), (x1 + tw + 6, y1), color, -1)
                cv2.putText(annotated, label, (x1 + 3, y1 - 3),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness + 1)
        if self.is_pose and result.keypoints is not None and result.keypoints.xy is not None:
            for kpts in result.keypoints.xy.cpu().numpy():
                for kp in kpts:
                    if kp[0] > 0 and kp[1] > 0:
                        cv2.circle(annotated, (int(kp[0]), int(kp[1])), 4, (255, 255, 0), -1)
        return annotated

    def _render_circle_annotated(self, frame: np.ndarray, result, iou_threshold: float) -> np.ndarray:
        annotated = frame.copy()
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            boxes_np = boxes.xyxy.cpu().numpy()
            overlapping = self._find_overlapping(boxes_np, iou_threshold)
            for i, box in enumerate(boxes_np):
                x1, y1, x2, y2 = box.astype(int)
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                bw, bh = x2 - x1, y2 - y1
                color = (0, 140, 255) if i in overlapping else (0, 0, 200)
                label = str(i + 1)
                radius = max(4, min(int(min(bw, bh) * 0.15), 40))
                font_scale = max(0.3, min(radius / 18.0, 1.2))
                thickness = max(1, int(radius / 10))
                cv2.circle(annotated, (cx, cy), radius, color, -1)
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
                cv2.putText(annotated, label, (cx - tw // 2, cy + th // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        if self.is_pose and result.keypoints is not None and result.keypoints.xy is not None:
            for kpts in result.keypoints.xy.cpu().numpy():
                for kp in kpts:
                    if kp[0] > 0 and kp[1] > 0:
                        cv2.circle(annotated, (int(kp[0]), int(kp[1])), 4, (255, 255, 0), -1)
        return annotated
