import cv2


def draw_recognized_face(
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
    verified,
    verifier
):

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        2
    )

    cv2.putText(
        frame,
        student_code,
        (x1, y1 - 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
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
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Blinks: {blink_count}",
        (x1, y2 + 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
        2
    )

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
        (0, 255, 0)
        if verified
        else
        (0, 0, 255)
    )

    cv2.putText(
        frame,
        f"Pose: {direction}",
        (x1, y2 + 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 0),
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

def draw_unknown_face(
    frame,
    x1,
    y1,
    x2,
    y2
):

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