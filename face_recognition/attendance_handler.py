import time

from attendance.attendance import (
    mark_attendance
)


def process_attendance(
    student_id,
    student_code,
    full_name,
    session_id,
    attendance_cache
):
    """
    Ghi điểm danh nếu đủ điều kiện
    """

    current_timestamp = time.time()

    last_seen = attendance_cache.get(
        student_id,
        0
    )

    if current_timestamp - last_seen <= 10:

        return

    success = mark_attendance(
        session_id=session_id,
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