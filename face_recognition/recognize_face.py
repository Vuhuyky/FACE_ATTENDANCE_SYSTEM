import cv2

from datetime import datetime
from insightface.app import FaceAnalysis

from database.connection import get_connection, PHOTOS_DIR

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

# ==========================================
# Global variables
# ==========================================

app = None

students = []

current_session_id = None

section_id = None

attendance_cache = {}

verified_cache = {}

blink_counters = {}

liveness_verifiers = {}


# ==========================================
# Initialize
# ==========================================

def initialize():

    global app
    global students
    global current_session_id
    global section_id
    global attendance_cache
    global verified_cache
    global blink_counters
    global liveness_verifiers

    attendance_cache = {}
    verified_cache = {}
    blink_counters = {}
    liveness_verifiers = {}

    auto_session_manager()

    current_session_id = get_current_session()

    if current_session_id is None:

        print("No active session found")

        return False

    section_id = get_session_section(
        current_session_id
    )

    print("Current Session:", current_session_id)
    print("Section:", section_id)

    app = FaceAnalysis()

    app.prepare(
        ctx_id=0,
        det_size=(640, 640)
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            s.id,
            s.student_code,
            s.full_name,

            c.course_name,

            cs.section_name,

            cs.room,

            s.photo_path,

            s.face_embedding

        FROM students s

        JOIN enrollments e
            ON s.id = e.student_id

        JOIN course_sections cs
            ON e.section_id = cs.id

        JOIN courses c
            ON cs.course_id = c.id

        WHERE
            e.section_id = ?
            AND s.face_embedding IS NOT NULL
        """,
        (section_id,)
    )

    rows = cursor.fetchall()

    students = []

    for row in rows:

        students.append(
            (
                row[0],      # student_id
                row[1],      # student_code
                row[2],      # full_name

                row[3],      # course_name

                row[4],      # section_name

                row[5],      # room

                row[6],      # photo_path (filename only, or None)

                json_to_embedding(row[7])   # embedding - always LAST
            )
        )

    conn.close()

    print(f"Loaded {len(students)} students")

    return True


# ==========================================
# Process One Frame
# ==========================================

def process_frame(frame):

    global attendance_cache
    global verified_cache
    global blink_counters
    global liveness_verifiers

    info = None

    best_student = None
    similarity = 0
    student_id = None
    student_code = None
    full_name = None
    course_name = None
    section_name = None
    room = None
    photo_path = None
    verified = False

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

            course_name = best_student[3]

            section_name = best_student[4]

            room = best_student[5]

            photo_path = best_student[6]

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
                # VERIFIED (detect the moment
                # it FIRST becomes true)
                # ==========================

                if (
                    liveness_verifiers[
                        student_id
                    ].is_verified()
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

            verified = verified_cache.get(
                student_id,
                False
            )

            if verified:

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

    if best_student is not None:
        photo_full_path = (
            str(PHOTOS_DIR / photo_path)
            if photo_path else None
        )

        info = {
            "student_id": student_id,
            "student_code": student_code,
            "full_name": full_name,
            "course": course_name,
            "section": section_name,
            "room": room,
            "photo_path": photo_full_path,
            "verified": verified,
            "similarity": similarity,
            "status": "Present" if verified else "Verifying...",
            "time": current_time
        }

    return frame, info


# ==========================================
# Main loop
# ==========================================

if __name__ == "__main__":

    if not initialize():

        print("Could not start: no active session.")

    else:

        cap = cv2.VideoCapture(
            0,
            cv2.CAP_DSHOW
        )

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            frame, info = process_frame(frame)

            cv2.imshow(
                "Face Recognition",
                frame
            )

            if cv2.waitKey(1) == 27:
                break

        cap.release()

        cv2.destroyAllWindows()