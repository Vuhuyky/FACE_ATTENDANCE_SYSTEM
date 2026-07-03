import cv2


class CameraService:

    def __init__(

        self,

        camera_index=0,

        width=1280,

        height=720

    ):

        self.camera_index = camera_index

        self.width = width

        self.height = height

        self.cap = None


    # ============================================
    # Open Camera
    # ============================================

    def start(self):

        self.cap = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_DSHOW
        )

        if not self.cap.isOpened():

            raise Exception(
                "Cannot open camera."
            )

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.width
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.height
        )
        self.cap.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )

    # ============================================
    # Read Frame
    # ============================================

    def get_frame(self):

        if self.cap is None:

            return None

        ret, frame = self.cap.read()

        if not ret:

            return None

        return frame


    # ============================================
    # Release Camera
    # ============================================

    def stop(self):

        if self.cap is not None:

            self.cap.release()

            self.cap = None


    # ============================================
    # Camera Status
    # ============================================

    def is_opened(self):

        return (

            self.cap is not None

            and

            self.cap.isOpened()

        )