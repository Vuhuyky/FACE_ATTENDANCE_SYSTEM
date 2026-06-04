import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def start_recognition():

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "face_recognition.recognize_face"
        ]
    )


def create_session():

    subprocess.run(
        [
            sys.executable,
            "attendance/create_session.py"
        ]
    )

    messagebox.showinfo(
        "Success",
        "Session created!"
    )


def show_report():

    subprocess.run(
        [
            sys.executable,
            "attendance/attendance_report.py"
        ]
    )


def export_excel():

    subprocess.run(
        [
            sys.executable,
            "attendance/export_excel.py"
        ]
    )

    messagebox.showinfo(
        "Success",
        "Excel exported!"
    )


root = tk.Tk()

root.title(
    "Face Attendance System"
)

root.geometry(
    "500x400"
)


title = tk.Label(
    root,
    text="FACE ATTENDANCE SYSTEM",
    font=("Arial", 18, "bold")
)

title.pack(
    pady=20
)


btn1 = tk.Button(
    root,
    text="Start Recognition",
    width=25,
    height=2,
    command=start_recognition
)

btn1.pack(
    pady=10
)


btn2 = tk.Button(
    root,
    text="Create Session",
    width=25,
    height=2,
    command=create_session
)

btn2.pack(
    pady=10
)


btn3 = tk.Button(
    root,
    text="Attendance Report",
    width=25,
    height=2,
    command=show_report
)

btn3.pack(
    pady=10
)


btn4 = tk.Button(
    root,
    text="Export Excel",
    width=25,
    height=2,
    command=export_excel
)

btn4.pack(
    pady=10
)


btn5 = tk.Button(
    root,
    text="Exit",
    width=25,
    height=2,
    command=root.destroy
)

btn5.pack(
    pady=10
)


root.mainloop()