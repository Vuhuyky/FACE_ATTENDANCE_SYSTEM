import cv2
import sqlite3
from datetime import datetime
from insightface.app import FaceAnalysis
import time

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
                (x2, y2 - 220),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
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