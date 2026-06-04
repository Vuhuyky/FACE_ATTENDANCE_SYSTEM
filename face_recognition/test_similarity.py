import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0)

cap = cv2.VideoCapture(0)

embeddings = []

print("Press SPACE to capture")
print("Need 2 captures")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Capture Face", frame)

    key = cv2.waitKey(1)

    if key == 32:  # SPACE

        faces = app.get(frame)

        if len(faces) > 0:

            embeddings.append(faces[0].embedding)

            print(f"Captured {len(embeddings)}")

        if len(embeddings) == 2:
            break

cap.release()
cv2.destroyAllWindows()

e1 = embeddings[0]
e2 = embeddings[1]

similarity = np.dot(
    e1 / np.linalg.norm(e1),
    e2 / np.linalg.norm(e2)
)

print()
print("Cosine Similarity:")
print(similarity)