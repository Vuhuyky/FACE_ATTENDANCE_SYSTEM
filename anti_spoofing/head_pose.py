import numpy as np


def get_head_direction(face):

    kps = face.kps

    left_eye = kps[0]
    right_eye = kps[1]
    nose = kps[2]

    eye_center_x = (
        left_eye[0] +
        right_eye[0]
    ) / 2

    offset = (
        nose[0] -
        eye_center_x
    )

    if offset > 10:
        return "RIGHT"

    elif offset < -10:
        return "LEFT"

        return "LEFT"

    return "CENTER"