import cv2

from insightface.app import FaceAnalysis

from anti_spoofing.head_pose import (
    get_head_direction
)

# ==========================================
# Khởi tạo InsightFace
# ==========================================

app = FaceAnalysis()

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

# ==========================================
# Mở camera
# ==========================================

cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

if not cap.isOpened():

    print(
        "Cannot open camera"
    )

    exit()

# ==========================================
# Vòng lặp realtime
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:

        print(
            "Cannot read frame"
        )

        continue

    faces = app.get(frame)

    # ======================================
    # Hiển thị số khuôn mặt
    # ======================================

    cv2.putText(
        frame,
        f"Faces: {len(faces)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    # ======================================
    # Xử lý từng khuôn mặt
    # ======================================

    for face in faces:

        direction = get_head_direction(
            face
        )

        # ==================================
        # Bounding Box
        # ==================================

        box = face.bbox.astype(int)

        x1, y1, x2, y2 = box

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # ==================================
        # Hiển thị hướng đầu
        # ==================================

        cv2.putText(
            frame,
            f"HEAD: {direction}",
            (x1, y1 - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # ==================================
        # Hiển thị 5 keypoints
        # ==================================

        for point in face.kps:

            x = int(point[0])
            y = int(point[1])

            cv2.circle(
                frame,
                (x, y),
                3,
                (0, 255, 255),
                -1
            )

    # ======================================
    # Hiển thị frame
    # ======================================

    cv2.imshow(
        "Head Pose Test",
        frame
    )

    # ESC để thoát

    if cv2.waitKey(1) == 27:

        break

# ==========================================
# Giải phóng tài nguyên
# ==========================================

cap.release()

cv2.destroyAllWindows()