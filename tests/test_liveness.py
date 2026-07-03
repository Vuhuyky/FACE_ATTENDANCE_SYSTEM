from liveness_verifier import (
    LivenessVerifier
)

lv = LivenessVerifier()

print(
    lv.is_verified()
)

lv.update_blink()

print(
    lv.is_verified()
)

lv.update_head_pose(
    "LEFT"
)

print(
    lv.is_verified()
)

lv.update_head_pose(
    "RIGHT"
)

print(
    lv.is_verified()
)