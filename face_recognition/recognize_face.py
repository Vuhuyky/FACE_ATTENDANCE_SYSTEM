import cv2
import sqlite3
from datetime import datetime
from insightface.app import FaceAnalysis
import time

from face_recognition.draw_face_info import draw_face_info

from face_recognition.draw_utils import (
    draw_recognized_face,
    draw_unknown_face
)

from attendance.attendance import (
    mark_attendance
)

from attendance.get_current_session import (
    get_current_session
)

from face_recognition.utils import (
    json_to_embedding,
    find_best_match
)

from anti_spoofing.blink_counter import BlinkCounter

from anti_spoofing.liveness_verifier import (
    LivenessVerifier
)

from anti_spoofing.blink_detector import (
    get_eye_landmarks,
    calculate_ear
)
from anti_spoofing.head_pose import (
    get_head_direction
)
# ==========================================
# 1. Khởi tạo InsightFace
# ==========================================

app = FaceAnalysis()

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

# ==========================================
# 2. Load toàn bộ sinh viên đã đăng ký mặt
# từ database
# ==========================================

conn = sqlite3.connect(
    "attendance.db"
)

cursor = conn.cursor()

cursor.execute("""
SELECT
    id,
    student_code,
    full_name,
    face_embedding
FROM students
WHERE face_embedding IS NOT NULL
""")

rows = cursor.fetchall()

students = []

for row in rows:

    student_id = row[0]
    student_code = row[1]
    full_name = row[2]
    embedding_json = row[3]

    students.append(
        (
            row[0],  # student_id
            row[1],  # student_code
            row[2],  # full_name
            json_to_embedding(
                row[3]
            )  # face_embedding
        )
    )

conn.close()

print(
    f"Loaded {len(students)} students"
)

# ==========================================
# 3. Mở camera
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

attendance_cache = {} 

verified_cache = {}

blink_counters = {}

liveness_verifiers = {}

current_session_id = (
    get_current_session()
)

print(
    "Current Session:",
    current_session_id
)

if current_session_id is None:

    print(
        "No active session found"
    )

    exit()
# ==========================================
# 4. Vòng lặp realtime
# ==========================================

while True:

    # Đọc frame từ camera
    ret, frame = cap.read()

    if not ret:
        break

    # ======================================
    # Detect tất cả khuôn mặt trong frame
    # ======================================

    faces = app.get(frame)
    cv2.putText(
    frame,
    f"Faces: {len(faces)}",
    (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 0, 0),
    2
    )

    current_time = datetime.now().strftime(
    "%Y-%m-%d %H:%M:%S"
    )

    cv2.putText(
    frame,
    current_time,
    (10, 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (255, 255, 255),
    2
    )

    # ======================================
    # Xử lý từng khuôn mặt
    # ======================================

    for face in faces:

        # Embedding của khuôn mặt hiện tại
        current_embedding = face.embedding

        # Tìm sinh viên giống nhất
        best_student, similarity = (
            find_best_match(
                current_embedding,
                students
            )
        )

        # Lấy tọa độ bounding box
        box = face.bbox.astype(int)

        x1, y1, x2, y2 = box

        # ==================================
        # Nếu nhận diện thành công
        # ==================================

        if best_student is not None:

            student_id = best_student[0]

            student_code = best_student[1]

            full_name = best_student[2]

            # ==========================
            # Blink Detection
            # ==========================

            if student_id not in blink_counters:

                blink_counters[
                    student_id
                ] = BlinkCounter()

            if student_id not in liveness_verifiers:

                liveness_verifiers[
                    student_id
                ] = LivenessVerifier()

            result = get_eye_landmarks(
                face
            )

            ear = 0

            blink_detected = False

            verified = False

            direction = "CENTER"

            if result:

                left_eye, right_eye = result

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

                blink_detected = (
                    blink_counters[
                        student_id
                    ].update(
                        ear
                    )
                )

                if (
                    blink_detected
                    and
                    not liveness_verifiers[
                        student_id
                    ].blinked
                ):

                    liveness_verifiers[
                        student_id
                    ].update_blink()
                    print(
                        "BLINK STATE =",
                        liveness_verifiers[
                            student_id
                        ].blinked
                    )
                    print(
                        f"{student_code} BLINK OK"
                    )

                # ==========================
                # HEAD POSE
                # ==========================

                direction = get_head_direction(
                    face
                )

                if (
                    direction == "LEFT"
                    and not liveness_verifiers[
                        student_id
                    ].looked_left
                ):

                    print(
                        "LEFT DETECTED"
                    )

                    liveness_verifiers[
                        student_id
                    ].update_head_pose(
                        "LEFT"
                    )

                elif (
                    direction == "RIGHT"
                    and not liveness_verifiers[
                        student_id
                    ].looked_right
                ):

                    print(
                        "RIGHT DETECTED"
                    )

                    liveness_verifiers[
                        student_id
                    ].update_head_pose(
                        "RIGHT"
                    )
                # ==========================
                # VERIFIED
                # ==========================

                verified = (
                    liveness_verifiers[
                        student_id
                    ].is_verified()
                )
                
                if (
                    verified
                    and not verified_cache.get(
                        student_id,
                        False
                    )
                ):

                    print(
                        f"[VERIFIED] "
                        f"{student_code}"
                    )

                    verified_cache[
                        student_id
                    ] = True

            if verified_cache.get(student_id, False):

                current_timestamp = time.time()

                last_seen = attendance_cache.get(
                    student_id,
                    0
                )

                if current_timestamp - last_seen > 10:

                    success = mark_attendance(
                        session_id=current_session_id,
                        student_id=student_id
                    )

                    if success:

                        print(
                            f"[ATTENDANCE] "
                            f"{student_code} - "
                            f"{full_name}"
                        )

                    attendance_cache[
                        student_id
                    ] = current_timestamp
            # ==========================
            # Màu sắc theo độ tin cậy
            # ==========================

            if similarity >= 0.8:

                color = (0, 255, 0)

            elif similarity >= 0.6:

                color = (0, 255, 255)

            else:

                color = (0, 0, 255)

    # ==========================
    # Vẽ khung mặt
    # ==========================

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

    # ==========================
    # Mã sinh viên
    # ==========================

            cv2.putText(
                frame,
                student_code,
                (x1, y1 - 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

    # ==========================
    # Họ tên
    # ==========================

            cv2.putText(
                frame,
                full_name,
                (x1, y1 - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    # ==========================
    # Điểm similarity
    # ==========================
            cv2.putText(
                frame,
                f"{similarity:.2f}",
                (x1, y1 - 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            cv2.putText(
                frame,
                f"EAR: {ear:.2f}",
                (x1, y2 + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,0),
                # color,
                2
            )

            cv2.putText(
                frame,
                f"Blinks: {blink_counters[student_id].total_blinks}",
                (x1, y2 + 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,0),
                # color,
                2
            )

            # status_text = (
            #     "VERIFIED"
            #     if verified
            #     else
            #     "PLEASE BLINK"
            # )
            verifier = liveness_verifiers[
                student_id
            ]

            if verified:

                status_text = "VERIFIED"

            elif not verifier.blinked:

                status_text = "PLEASE BLINK"

            elif not verifier.looked_left:

                status_text = "TURN LEFT"

            elif not verifier.looked_right:

                status_text = "TURN RIGHT"

            else:

                status_text = "VERIFYING..."
            status_color = (
                (0,255,0)
                if verified
                else
                (0,0,255)
            )
            cv2.putText(
                frame,
                f"Pose: {direction}",
                (x1, y2 + 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255,255,0),
                2
            )
            cv2.putText(
                frame,
                status_text,
                (x1, y2 + 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                status_color,
                2
            )
        # ==================================
        # Nếu không nhận diện được
        # ==================================

        else:

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                "Unknown",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

    # ======================================
    # Hiển thị frame sau khi xử lý
    # ======================================

    cv2.imshow(
        "Face Recognition",
        frame
    )

    # ESC để thoát
    if cv2.waitKey(1) == 27:
        break

# ==========================================
# 5. Giải phóng camera
# ==========================================

cap.release()

cv2.destroyAllWindows()