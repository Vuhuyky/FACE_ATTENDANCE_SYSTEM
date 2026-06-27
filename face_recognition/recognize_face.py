import cv2
import sqlite3
from datetime import datetime
from insightface.app import FaceAnalysis
import time
from database.connection import get_connection

from face_recognition.draw_face_info import draw_face_info

from face_recognition.draw_utils import (
    draw_recognized_face,
    draw_unknown_face
)

from face_recognition.attendance_handler import (
    process_attendance
)

from attendance.attendance import (
    mark_attendance
)

from database.get_session_section import (
    get_session_section
)

from database.auto_session_manager import (
    auto_session_manager
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
auto_session_manager()

current_session_id = (
    get_current_session()
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
current_session_id = (
    get_current_session()
)

section_id = get_session_section(
    current_session_id
)

print(
    "Current Session:",
    current_session_id
)

print(
    "Section:",
    section_id
)

conn = get_connection()

cursor = conn.cursor()

cursor.execute(
    """
    SELECT
        s.id,
        s.student_code,
        s.full_name,
        s.face_embedding
    FROM students s

    JOIN enrollments e
        ON s.id = e.student_id

    WHERE e.section_id = ?
    AND s.face_embedding IS NOT NULL
    """,
    (section_id,)
)

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
section_id = (
    get_session_section(
        current_session_id
    )
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
            if verified_cache.get(
                student_id,
                False
            ):

                process_attendance(
                    student_id=student_id,
                    student_code=student_code,
                    full_name=full_name,
                    session_id=current_session_id,
                    attendance_cache=attendance_cache
                )
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

            draw_recognized_face(
                frame=frame,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                color=color,
                student_code=student_code,
                full_name=full_name,
                similarity=similarity,
                ear=ear,
                blink_count=blink_counters[
                    student_id
                ].total_blinks,
                direction=direction,
                verified=verified,
                verifier=liveness_verifiers[
                    student_id
                ]
            )
        # ==================================
        # Nếu không nhận diện được
        # ==================================

        else:

            draw_unknown_face(
                frame,
                x1,
                y1,
                x2,
                y2
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