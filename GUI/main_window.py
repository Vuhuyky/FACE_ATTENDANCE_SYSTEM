import tkinter as tk
from tkinter import messagebox
import subprocess
import sys


def open_module(module_name):

    try:
        subprocess.Popen(
            [
                sys.executable,
                "-m",
                module_name
            ]
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


def exit_program():

    if messagebox.askyesno(
        "Exit",
        "Do you want to exit?"
    ):

        root.destroy()


root = tk.Tk()

root.title("Face Attendance System")

root.geometry("700x550")

root.resizable(False, False)


# ===========================
# Title
# ===========================

title = tk.Label(
    root,
    text="FACE ATTENDANCE SYSTEM",
    font=("Arial", 22, "bold"),
    fg="blue"
)

title.pack(
    pady=20
)


# ===========================
# Menu Frame
# ===========================

frame = tk.Frame(root)

frame.pack(
    pady=20
)


button_width = 22
button_height = 2


# ===========================
# Row 1
# ===========================

tk.Button(

    frame,

    text="Student Manager",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.student_management"
    )

).grid(
    row=0,
    column=0,
    padx=15,
    pady=10
)


tk.Button(

    frame,

    text="Course Manager",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.course_manager"
    )

).grid(
    row=0,
    column=1,
    padx=15,
    pady=10
)


# ===========================
# Row 2
# ===========================

tk.Button(

    frame,

    text="Section Manager",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.section_manager"
    )

).grid(
    row=1,
    column=0,
    padx=15,
    pady=10
)


tk.Button(

    frame,

    text="Schedule Manager",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.schedule_manager"
    )

).grid(
    row=1,
    column=1,
    padx=15,
    pady=10
)


# ===========================
# Row 3
# ===========================

tk.Button(

    frame,

    text="Enrollment Manager",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.enrollment_manager"
    )

).grid(
    row=2,
    column=0,
    padx=15,
    pady=10
)


tk.Button(

    frame,

    text="Session Manager",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.session_manager"
    )

).grid(
    row=2,
    column=1,
    padx=15,
    pady=10
)


# ===========================
# Row 4
# ===========================

tk.Button(

    frame,

    text="Register Face",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "face_recognition.register_face"
    )

).grid(
    row=3,
    column=0,
    padx=15,
    pady=10
)


tk.Button(

    frame,

    text="Attendance",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.attendance_gui"
    )

).grid(
    row=3,
    column=1,
    padx=15,
    pady=10
)


# ===========================
# Row 5
# ===========================

tk.Button(

    frame,

    text="Attendance Report",

    width=button_width,

    height=button_height,

    command=lambda: open_module(
        "GUI.attendance_report_gui"
    )

).grid(
    row=4,
    column=0,
    padx=15,
    pady=10
)


tk.Button(

    frame,

    text="Exit",

    width=button_width,

    height=button_height,

    bg="red",

    fg="white",

    command=exit_program

).grid(
    row=4,
    column=1,
    padx=15,
    pady=10
)


# ===========================

tk.Label(

    root,

    text="Graduation Project - Face Attendance System",

    font=("Arial", 10),

    fg="gray"

).pack(
    side="bottom",
    pady=15
)


root.mainloop()