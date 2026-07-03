from attendance.camera_service import CameraService

import cv2

camera = CameraService()

camera.start()

while True:

    frame = camera.get_frame()

    if frame is None:

        break

    cv2.imshow(
        "Camera",
        frame
    )

    if cv2.waitKey(1) == 27:

        break

camera.stop()

cv2.destroyAllWindows()