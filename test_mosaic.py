import cv2
import numpy as np

VIDEO = "warehouse.mp4"

cap = cv2.VideoCapture(VIDEO)

ret, prev_frame = cap.read()

if not ret:
    raise Exception("Cannot open video")

prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create(
    nfeatures=5000,
    scaleFactor=1.2,
    nlevels=8
)

matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

global_H = np.eye(3)

camera_points = []

frame_id = 0

FRAME_STEP = 3

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_id += 1

    if frame_id % FRAME_STEP != 0:
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kp1, des1 = orb.detectAndCompute(prev_gray, None)
    kp2, des2 = orb.detectAndCompute(gray, None)

    if des1 is None or des2 is None:
        print("No descriptors")
        prev_gray = gray
        continue

    matches = matcher.knnMatch(des1, des2, k=2)

    good = []

    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append(m)

    print(
        f"Frame={frame_id}  "
        f"KP1={len(kp1)}  "
        f"KP2={len(kp2)}  "
        f"Good={len(good)}"
    )

    if len(good) < 25:
        prev_gray = gray
        continue

    pts1 = np.float32(
        [kp1[m.queryIdx].pt for m in good]
    ).reshape(-1, 1, 2)

    pts2 = np.float32(
        [kp2[m.trainIdx].pt for m in good]
    ).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(
        pts1,
        pts2,
        cv2.RANSAC,
        5.0
    )

    if H is None:
        print("Homography failed")
        prev_gray = gray
        continue

    global_H = global_H @ np.linalg.inv(H)

    pos = global_H @ np.array([0, 0, 1])

    pos = pos / pos[2]

    camera_points.append(
        (
            float(pos[0]),
            float(pos[1])
        )
    )

    # -----------------------
    # Draw path
    # -----------------------

    canvas = np.zeros(
        (1000, 1000, 3),
        dtype=np.uint8
    )

    if len(camera_points) > 1:

        xs = [p[0] for p in camera_points]
        ys = [p[1] for p in camera_points]

        min_x = min(xs)
        max_x = max(xs)

        min_y = min(ys)
        max_y = max(ys)

        range_x = max(max_x - min_x, 1)
        range_y = max(max_y - min_y, 1)

        scale = min(
            800 / range_x,
            800 / range_y
        )

        draw_points = []

        for x, y in camera_points:

            dx = int(
                (x - min_x) * scale + 100
            )

            dy = int(
                (y - min_y) * scale + 100
            )

            draw_points.append((dx, dy))

        for i in range(1, len(draw_points)):

            cv2.line(
                canvas,
                draw_points[i - 1],
                draw_points[i],
                (0, 255, 0),
                2
            )

        cv2.circle(
            canvas,
            draw_points[-1],
            6,
            (0, 0, 255),
            -1
        )

    cv2.putText(
        canvas,
        f"Frames: {frame_id}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Camera Path",
        canvas
    )

    # -----------------------
    # Draw Matches
    # -----------------------

    match_vis = cv2.drawMatches(
        prev_gray,
        kp1,
        gray,
        kp2,
        good[:50],
        None,
        flags=2
    )

    match_vis = cv2.resize(
        match_vis,
        (1400, 700)
    )

    cv2.imshow(
        "Matches",
        match_vis
    )

    key = cv2.waitKey(1)

    if key == 27:
        break

    prev_gray = gray

cap.release()
cv2.destroyAllWindows()