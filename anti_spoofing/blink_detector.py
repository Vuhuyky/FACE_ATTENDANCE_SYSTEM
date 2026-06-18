import numpy as np


def euclidean(p1, p2):

    return np.linalg.norm(
        p1 - p2
    )


def calculate_ear(eye):

    A = euclidean(
        eye[1],
        eye[5]
    )

    B = euclidean(
        eye[2],
        eye[4]
    )

    C = euclidean(
        eye[0],
        eye[3]
    )

    ear = (A + B) / (2.0 * C)

    return ear


def get_eye_landmarks(face):

    if not hasattr(
        face,
        "landmark_3d_68"
    ):
        return None

    landmarks = face.landmark_3d_68

    left_eye = landmarks[36:42]

    right_eye = landmarks[42:48]

    return (
        left_eye,
        right_eye
    )

blink_counter = 0

eye_closed = False

def detect_blink(
    ear,
    threshold=0.25
):
    global blink_counter
    global eye_closed

    if ear < threshold:

        eye_closed = True

    elif ear >= threshold and eye_closed:

        blink_counter += 1

        eye_closed = False

        return True

    return False