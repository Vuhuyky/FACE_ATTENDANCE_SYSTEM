import cv2
import sqlite3
import numpy as np

from insightface.app import FaceAnalysis

from utils import embedding_to_json


# =====================
# Load Face Model
# =====================

app = FaceAnalysis(name="buffalo_l")

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

# =====================
# Input MSSV
# =====================

student_code = input(
    "Enter Student Code: "
)

# =====================
# Check Student Exists
# =====================

conn = sqlite3.connect(
    "attendance.db"
)

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
    (student_code,)
)

student = cursor.fetchone()

if student is None:

    print("Student not found!")

    conn.close()

    exit()

if student[2] is not None:

    print()
    answer = input(
        "Face already registered. Overwrite? (y/n): "
    )

    if answer.lower() != "y":

        print("Registration cancelled.")

        conn.close()

        exit()

print()
print(f"Student Code: {student_code}")
print(f"Student Name: {student[1]}")
print()

# =====================
# Open Camera
# =====================

cap = cv2.VideoCapture(0)

embeddings = []

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

    if key == 32:  # SPACE

        faces = app.get(frame)

        if len(faces) == 0:

            print("No face detected")

            continue

        embedding = faces[0].embedding

        embeddings.append(
            embedding
        )

        print(
            f"Captured {len(embeddings)}/5"
        )

        if len(embeddings) == 5:
            break

# =====================
# Release Camera
# =====================

cap.release()

cv2.destroyAllWindows()

# =====================
# Average Embedding
# =====================
if len(embeddings) != 5:

    print(
        "Registration failed!"
    )

    print(
        f"Captured only {len(embeddings)}/5"
    )

    conn.close()

    exit()

avg_embedding = np.mean(
    embeddings,
    axis=0
)

# =====================
# Save Database
# =====================

embedding_json = embedding_to_json(
    avg_embedding
)

cursor.execute(
    """
    UPDATE students
    SET face_embedding = ?
    WHERE student_code = ?
    """,
    (
        embedding_json,
        student_code
    )
)

conn.commit()

conn.close()

print()
print("Face registered successfully!")