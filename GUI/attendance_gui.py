import os

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import cv2

from PIL import Image
from PIL import ImageTk

from face_recognition.recognize_face import (
    initialize,
    process_frame
)


class AttendanceGUI:

    def __init__(self):

        self.engine_ready = initialize()

        self.root = tk.Tk()

        self.root.title(
            "Face Attendance System"
        )

        self.root.geometry(
            "1200x700"
        )

        self.root.resizable(
            False,
            False
        )

        self.cap = cv2.VideoCapture(
            0,
            cv2.CAP_DSHOW
        )

        tk.Label(
            self.root,
            text="FACE ATTENDANCE SYSTEM",
            font=("Arial", 20, "bold")
        ).pack(
            pady=10
        )

        main = tk.Frame(
            self.root
        )

        main.pack(
            fill="both",
            expand=True,
            padx=10
        )

        # ====================================
        # CAMERA FRAME
        # ====================================

        self.camera_frame = tk.LabelFrame(
            main,
            text="Camera",
            width=760,
            height=480
        )

        self.camera_frame.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.camera_frame.pack_propagate(
            False
        )

        self.camera_label = tk.Label(
            self.camera_frame,
            text="Loading Camera...",
            font=("Arial", 18)
        )

        self.camera_label.pack(
            expand=True
        )

        # ====================================
        # RIGHT PANEL
        # ====================================

        right = tk.LabelFrame(
            main,
            text="Student Information",
            width=380,
            height=480
        )

        right.pack(
            side="right",
            padx=10,
            pady=10,
            fill="y"
        )

        right.pack_propagate(
            False
        )

        self.vars = {}

        fields = [

            ("Student ID", "-"),

            ("Student Code", "-"),

            ("Name", "-"),

            ("Course", "-"),

            ("Section", "-"),

            ("Room", "-"),

            ("Time", "-"),

            ("Status", "Waiting...")

        ]

        for label, value in fields:

            tk.Label(
                right,
                text=label + ":",
                font=("Arial", 10, "bold")
            ).pack(
                anchor="w",
                padx=10,
                pady=(6, 0)
            )

            var = tk.StringVar(
                value=value
            )

            self.vars[label] = var

            tk.Label(
                right,
                textvariable=var,
                font=("Arial", 10)
            ).pack(
                anchor="w",
                padx=25
            )

        self.photo_frame = tk.Frame(
            right,
            width=100,
            height=110,
            relief="solid",
            bd=1
        )

        self.photo_frame.pack(
            pady=15
        )

        self.photo_frame.pack_propagate(
            False
        )

        self.photo = tk.Label(
            self.photo_frame,
            text="Student Photo"
        )

        self.photo.pack(
            fill="both",
            expand=True
        )

        self.current_photo_image = None

        self.last_photo_path = None

        self.status_label = tk.Label(
            right,
            text="READY",
            fg="blue",
            font=("Arial", 16, "bold")
        )

        self.status_label.pack()

        # ====================================
        # LOG FRAME
        # ====================================

        log_frame = tk.LabelFrame(
            self.root,
            text="Recognition Log"
        )

        log_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.log = ttk.Treeview(

            log_frame,

            columns=(
                "time",
                "id",
                "name",
                "status"
            ),

            show="headings",

            height=8

        )

        self.log.heading(
            "time",
            text="Time"
        )

        self.log.heading(
            "id",
            text="Student ID"
        )

        self.log.heading(
            "name",
            text="Name"
        )

        self.log.heading(
            "status",
            text="Status"
        )

        self.log.column(
            "time",
            width=120,
            anchor="center"
        )

        self.log.column(
            "id",
            width=120,
            anchor="center"
        )

        self.log.column(
            "name",
            width=260,
            anchor="center"
        )

        self.log.column(
            "status",
            width=120,
            anchor="center"
        )

        self.log.pack(
            fill="both",
            expand=True
        )

        self.last_student = None

        self.last_status = None

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        if not self.engine_ready:

            self.camera_label.configure(
                text="No active session.\nCannot start recognition.",
                image=""
            )

            self.status_label.config(
                text="NO SESSION",
                fg="red"
            )

            messagebox.showerror(
                "Attendance",
                "No active session found.\n"
                "Please start/select a session before "
                "taking attendance."
            )

        else:

            self.update_camera()

    # ====================================
    # UPDATE CAMERA
    # ====================================

    def update_camera(self):

        if not self.engine_ready:
            return

        ret, frame = self.cap.read()

        if ret:

            frame, info = process_frame(frame)

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(frame)

            image = image.resize(
                (
                    730,
                    440
                )
            )

            photo = ImageTk.PhotoImage(image)

            self.camera_label.configure(
                image=photo,
                text=""
            )

            self.camera_label.image = photo

            if info is not None:

                self.update_student_info(info)

        self.root.after(
            10,
            self.update_camera
        )

    # ====================================
    # UPDATE STUDENT PHOTO BOX
    # ====================================

    def update_student_photo(self, photo_path):

        # Nothing to show.
        if not photo_path:

            self.photo.configure(
                image="",
                text="No Photo"
            )

            self.current_photo_image = None
            self.last_photo_path = None

            return

        if photo_path == self.last_photo_path:

            return

        if not os.path.exists(photo_path):

            self.photo.configure(
                image="",
                text="No Photo"
            )

            self.current_photo_image = None
            self.last_photo_path = None

            return

        try:

            image = Image.open(photo_path)

            image.thumbnail(
                (
                    140,
                    140
                )
            )

            photo_image = ImageTk.PhotoImage(image)

            self.photo.configure(
                image=photo_image,
                text=""
            )

            # Keep a reference alive.
            self.current_photo_image = photo_image
            self.last_photo_path = photo_path

        except Exception as error:

            print(
                "Could not load student photo:",
                error
            )

            self.photo.configure(
                image="",
                text="No Photo"
            )

            self.current_photo_image = None
            self.last_photo_path = None

    # ====================================
    # UPDATE RIGHT PANEL
    # ====================================

    def update_student_info(self, info):

        self.vars["Student ID"].set(
            info["student_id"]
        )

        self.vars["Student Code"].set(
            info["student_code"]
        )

        self.vars["Name"].set(
            info["full_name"]
        )

        self.vars["Course"].set(
            info["course"]
        )

        self.vars["Section"].set(
            info["section"]
        )

        self.vars["Room"].set(
            info["room"]
        )

        self.vars["Time"].set(
            info["time"]
        )

        self.vars["Status"].set(
            info["status"]
        )

        self.update_student_photo(
            info.get("photo_path")
        )

        if info["verified"]:

            self.status_label.config(
                text="VERIFIED",
                fg="green"
            )

        else:

            self.status_label.config(
                text="VERIFYING...",
                fg="orange"

            )

        student_changed = (
            self.last_student != info["student_code"]
        )

        status_changed = (
            self.last_status != info["status"]
        )

        if student_changed or status_changed:

            self.add_log(

                info["time"],

                info["student_code"],

                info["full_name"],

                info["status"]

            )

            self.last_student = info["student_code"]

            self.last_status = info["status"]

    # ====================================
    # ADD LOG
    # ====================================

    def add_log(

        self,

        time,

        student_code,

        full_name,

        status

    ):

        self.log.insert(

            "",

            0,

            values=(

                time,

                student_code,

                full_name,

                status

            )

        )

    # ====================================
    # CLOSE
    # ====================================

    def on_close(self):

        if self.cap.isOpened():

            self.cap.release()

        self.root.destroy()

    # ====================================
    # RUN
    # ====================================

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    gui = AttendanceGUI()

    gui.run()