from ultralytics import YOLO
import cv2

model = YOLO("models/YOLO26s-1920-150epoch.pt")

cap = cv2.VideoCapture("videos/sample.mp4")

if not cap.isOpened():
    print("Error: Could not open video file")
    exit()

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

results = model.track(
    source="videos/sample.mp4",
    tracker="bytetrack.yaml",
    conf=0.5,
    persist=True,
    stream=True
)

seen_ids = set()

for r in results:
    frame = r.orig_img.copy()

    if r.boxes.id is not None:
        boxes = r.boxes.xyxy.cpu().numpy().astype(int)
        ids = r.boxes.id.cpu().numpy().astype(int)

        for box, track_id in zip(boxes, ids):
            x1, y1, x2, y2 = box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            cv2.putText(
                frame,
                str(track_id),
                (center_x - 15, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                2
            )

            if track_id not in seen_ids:
                print(f"New track ID detected: {track_id}")
                seen_ids.add(track_id)

    cv2.putText(
        frame,
        f"Unique Count: {len(seen_ids)}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    print(f"Current count: {len(seen_ids)}")
    cv2.imshow("YOLO Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("Final count:", len(seen_ids))