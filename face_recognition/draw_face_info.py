import cv2


def draw_face_info(
    frame,
    x1,
    y1,
    x2,
    y2,
    color,
    student_code,
    full_name,
    similarity,
    ear,
    blink_count,
    direction,
    status_text,
    status_color
):

    # ==========================
    # Face Box
    # ==========================

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        2
    )

    # ==========================
    # Student Info
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
        student_code,
        (x1, y1 - 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2
    )

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
    # Liveness Info
    # ==========================

    cv2.putText(
        frame,
        f"EAR: {ear:.2f}",
        (x1, y2 + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Blinks: {blink_count}",
        (x1, y2 + 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Pose: {direction}",
        (x1, y2 + 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    # ==========================
    # Status
    # ==========================

    cv2.putText(
        frame,
        status_text,
        (x1, y2 + 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        status_color,
        2
    )