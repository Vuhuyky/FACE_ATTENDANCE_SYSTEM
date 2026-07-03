import cv2
import sqlite3
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from insightface.app import FaceAnalysis

from .utils import embedding_to_json

from database.connection import get_connection, PHOTOS_DIR

# =====================
# Load Face Model
# =====================

app = FaceAnalysis(name="buffalo_l")

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


# =====================
# Load Students
# =====================

def load_students():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            student_code,
            full_name
        FROM students
        ORDER BY student_code
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =====================
# Register Face
# =====================

def register_face():

    student_text = combo_student.get()

    if not student_text:

        messagebox.showerror(
            "Error",
            "Please select student"
        )

        return

    student_code = student_text.split(" - ")[0]

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            full_name,
            face_embedding
        FROM students
        WHERE student_code = ?
        """,
        (
            student_code,
        )
    )

    student = cursor.fetchone()

    if student is None:

        messagebox.showerror(
            "Error",
            "Student not found"
        )

        conn.close()

        return

    if student[2] is not None:

        answer = messagebox.askyesno(
            "Warning",
            "Face already registered.\nOverwrite?"
        )

        if not answer:

            conn.close()

            return

    embeddings = []

    photo_filename = None

    cap = cv2.VideoCapture(0)

    print()
    print("Press SPACE 5 times")
    print("Look different directions")
    print()

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        cv2.imshow(
            "Register Face",
            frame
        )

        key = cv2.waitKey(1)

        if key == 32:

            faces = app.get(frame)

            if len(faces) == 0:

                print(
                    "No face detected"
                )

                continue

            embedding = faces[0].embedding

            embeddings.append(
                embedding
            )

            # ==========================
            # Save a photo the FIRST time
            # we successfully capture a
            # face for this student.
            # ==========================

            if photo_filename is None:

                box = faces[0].bbox.astype(int)

                x1, y1, x2, y2 = box

                x1 = max(x1, 0)
                y1 = max(y1, 0)

                face_crop = frame[y1:y2, x1:x2]

                if face_crop.size > 0:

                    photo_filename = (
                        f"{student_code}.jpg"
                    )

                    photo_full_path = (
                        PHOTOS_DIR / photo_filename
                    )

                    cv2.imwrite(
                        str(photo_full_path),
                        face_crop
                    )

                    print(
                        f"Saved photo: {photo_full_path}"
                    )

            print(
                f"Captured {len(embeddings)}/5"
            )

            if len(embeddings) == 5:
                break

    cap.release()

    cv2.destroyAllWindows()

    if len(embeddings) != 5:

        messagebox.showerror(
            "Error",
            f"Captured only {len(embeddings)}/5 images"
        )

        conn.close()

        return

    avg_embedding = np.mean(
        embeddings,
        axis=0
    )

    embedding_json = embedding_to_json(
        avg_embedding
    )

    cursor.execute(
        """
        UPDATE students
        SET face_embedding = ?,
            photo_path = COALESCE(?, photo_path)
        WHERE student_code = ?
        """,
        (
            embedding_json,
            photo_filename,
            student_code
        )
    )

    conn.commit()

    conn.close()

    messagebox.showinfo(
        "Success",
        "Face registered successfully"
    )


# =====================
# GUI
# =====================

root = tk.Tk()

root.title(
    "Register Face"
)

root.geometry(
    "500x250"
)

tk.Label(
    root,
    text="Select Student",
    font=("Arial", 12)
).pack(
    pady=10
)

combo_student = ttk.Combobox(
    root,
    width=45,
    state="readonly"
)

students = load_students()

combo_student["values"] = [

    f"{row[0]} - {row[1]}"

    for row in students
]

combo_student.pack(
    pady=10
)

btn_register = tk.Button(
    root,
    text="Register Face",
    width=20,
    height=2,
    command=register_face
)

btn_register.pack(
    pady=20
)

root.mainloop()