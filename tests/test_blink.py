import cv2

from insightface.app import FaceAnalysis

from blink_counter import BlinkCounter

from blink_detector import (
    get_eye_landmarks,
    calculate_ear
)

# ==========================
# InsightFace
# ==========================

app = FaceAnalysis()

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

# ==========================
# Camera
# ==========================

cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

# ==========================
# Blink Counter
# ==========================

blink_counter = BlinkCounter()

# ==========================
# Main Loop
# ==========================

while True:

    ret, frame = cap.read()

    if not ret:

        print(
            "Cannot read camera frame"
        )

        continue

    faces = app.get(frame)

    for face in faces:

        result = get_eye_landmarks(face)

        if not result:
            continue

        left_eye, right_eye = result

        # ==========================
        # Tính EAR
        # ==========================

        left_ear = calculate_ear(
            left_eye
        )

        right_ear = calculate_ear(
            right_eye
        )

        ear = (
            left_ear +
            right_ear
        ) / 2

        # ==========================
        # Blink Detection
        # ==========================

        blink_detected = (
            blink_counter.update(ear)
        )

        if blink_detected:

            print(
                f"BLINK DETECTED | "
                f"TOTAL = {blink_counter.total_blinks}"
            )

        # ==========================
        # Hiển thị EAR
        # ==========================

        cv2.putText(
            frame,
            f"EAR: {ear:.3f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # ==========================
        # Hiển thị số lần blink
        # ==========================

        cv2.putText(
            frame,
            f"Blinks: {blink_counter.total_blinks}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # ==========================
        # Vẽ mắt phải
        # ==========================

        for point in right_eye:

            x = int(point[0])
            y = int(point[1])

            cv2.circle(
                frame,
                (x, y),
                2,
                (0, 255, 0),
                -1
            )

        # ==========================
        # Vẽ mắt trái
        # ==========================

        for point in left_eye:

            x = int(point[0])
            y = int(point[1])

            cv2.circle(
                frame,
                (x, y),
                2,
                (0, 255, 0),
                -1
            )

    cv2.imshow(
        "Blink Test",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()

cv2.destroyAllWindows()