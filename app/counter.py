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
        self.min_conf = 0.0
        self.include_low_conf = True

    def _predict_kwargs(self, conf: float | None = None, iou: float | None = None, imgsz: int | None = None, include_low_conf: bool = True) -> dict:
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

    def count(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None, include_low_conf: bool = True):
        self.include_low_conf = include_low_conf

        conf_val = conf if conf is not None else self.conf_threshold
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        result = results[0]
        boxes = result.boxes

        if boxes is None or len(boxes) == 0:
            return {"count": 0, "dedup_count": 0, "low_conf_count": 0, "low_conf_detections": [], "filtered_count": 0, "detections": []}

        boxes_np = boxes.xyxy.cpu().numpy()
        count = len(boxes_np)
        confs = boxes.conf.cpu().numpy()
        kpts_data = []
        if self.is_pose and result.keypoints is not None and result.keypoints.xy is not None:
            kpts_data = result.keypoints.xy.cpu().numpy().tolist()

        detections = []
        low_conf_detections = []

        for i in range(count):
            conf_val = float(confs[i])
            detections.append({
                "bbox": boxes_np[i].tolist(),
                "confidence": round(conf_val, 3),
                "keypoints": kpts_data[i] if kpts_data else [],
            })

        # Deduplicate all detections
        high_conf_overlapping = self._find_overlapping(boxes_np, iou_val)
        dedup_count = len(boxes_np) - len(high_conf_overlapping)

        # Final count: all detections after deduplication
        filtered_count = dedup_count

        return {
            "count": count,
            "dedup_count": max(0, dedup_count),
            "low_conf_count": len(low_conf_detections),
            "low_conf_detections": low_conf_detections,
            "filtered_count": filtered_count,
            "detections": detections,
        }

    def draw_annotations(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None, include_low_conf: bool = True):
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        return self._render_bbox_annotated(image, results[0], iou_val, include_low_conf)

    def draw_circle_annotations(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None, include_low_conf: bool = True):
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        return self._render_circle_annotated(image, results[0], iou_val, include_low_conf)

    def draw_low_conf_bbox(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None, min_conf: float = 0.25):
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        return self._render_bbox_annotated_low_conf(image, results[0], iou_val, min_conf)

    def draw_low_conf_circle(self, image: np.ndarray, conf: float | None = None, iou: float | None = None, imgsz: int | None = None, min_conf: float = 0.25):
        iou_val = iou if iou is not None else self.iou_threshold
        results = self.model(image, **self._predict_kwargs(conf, iou_val, imgsz))
        return self._render_circle_annotated_low_conf(image, results[0], iou_val, min_conf)

    def _render_bbox_annotated(self, frame: np.ndarray, result, iou_threshold: float, include_low_conf: bool = True) -> np.ndarray:
        annotated = frame.copy()
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            boxes_np = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy().tolist()
            overlapping = self._find_overlapping(boxes_np, iou_threshold)
            for i, box in enumerate(boxes_np):
                x1, y1, x2, y2 = box.astype(int)
                is_duplicate = i in overlapping

                if is_duplicate:
                    color = (0, 140, 255)  # Orange for duplicates
                else:
                    color = (0, 0, 200)  # Blue for normal

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

    def _render_circle_annotated(self, frame: np.ndarray, result, iou_threshold: float, include_low_conf: bool = True) -> np.ndarray:
        annotated = frame.copy()
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            boxes_np = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy().tolist()
            overlapping = self._find_overlapping(boxes_np, iou_threshold)
            for i, box in enumerate(boxes_np):
                x1, y1, x2, y2 = box.astype(int)
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                is_duplicate = i in overlapping

                if is_duplicate:
                    color = (0, 140, 255)  # Orange for duplicates
                else:
                    color = (0, 0, 200)  # Blue for normal

                label = str(i + 1)
                bw, bh = x2 - x1, y2 - y1
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

    def _render_bbox_annotated_low_conf(self, frame: np.ndarray, result, iou_threshold: float, min_conf: float) -> np.ndarray:
        annotated = frame.copy()
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            boxes_np = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy().tolist()
            overlapping = self._find_overlapping(boxes_np, iou_threshold)
            for i, box in enumerate(boxes_np):
                x1, y1, x2, y2 = box.astype(int)
                conf_val = confs[i]
                is_low_conf = conf_val < min_conf
                is_duplicate = i in overlapping

                if is_low_conf:
                    color = (255, 100, 100)  # Red for low confidence
                elif is_duplicate:
                    color = (0, 140, 255)  # Orange for duplicates
                else:
                    color = (0, 0, 200)  # Blue for normal

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

    def _render_circle_annotated_low_conf(self, frame: np.ndarray, result, iou_threshold: float, min_conf: float) -> np.ndarray:
        annotated = frame.copy()
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            boxes_np = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy().tolist()
            overlapping = self._find_overlapping(boxes_np, iou_threshold)
            for i, box in enumerate(boxes_np):
                x1, y1, x2, y2 = box.astype(int)
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                conf_val = confs[i]
                is_low_conf = conf_val < min_conf
                is_duplicate = i in overlapping

                if is_low_conf:
                    color = (255, 100, 100)  # Red for low confidence
                elif is_duplicate:
                    color = (0, 140, 255)  # Orange for duplicates
                else:
                    color = (0, 0, 200)  # Blue for normal

                label = str(i + 1)
                bw, bh = x2 - x1, y2 - y1
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
