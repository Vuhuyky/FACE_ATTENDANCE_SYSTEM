class LivenessVerifier:

    def __init__(self):

        self.blinked = False

        self.looked_left = False

        self.looked_right = False

        self.verified = False

    def update_blink(self):

        self.blinked = True

    def update_head_pose(
        self,
        direction
    ):

        if direction == "LEFT":

            self.looked_left = True

        elif direction == "RIGHT":

            self.looked_right = True

    def is_verified(self):

        # print(
        #     "Blink:",
        #     self.blinked,
        #     "| Left:",
        #     self.looked_left,
        #     "| Right:",
        #     self.looked_right
        # )

        if (
            self.blinked
            and self.looked_left
            and self.looked_right
        ):

            self.verified = True

        return self.verified