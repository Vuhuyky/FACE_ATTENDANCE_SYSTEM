class BlinkCounter:

    def __init__(self):

        self.EAR_THRESHOLD = 0.27

        self.CONSEC_FRAMES = 2

        self.frame_counter = 0

        self.total_blinks = 0

    def update(self, ear):

        blink_detected = False

        if ear < self.EAR_THRESHOLD:

            self.frame_counter += 1

        else:

            if self.frame_counter >= self.CONSEC_FRAMES:

                self.total_blinks += 1

                blink_detected = True

            self.frame_counter = 0

        return blink_detected