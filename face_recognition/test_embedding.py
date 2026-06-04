import cv2
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l")

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    faces = app.get(frame)

    if len(faces) > 0:

        embedding = faces[0].embedding

        print("Embedding shape:", embedding.shape)

        print("First 10 values:")

        print(embedding[:10])

        break

cap.release()
cv2.destroyAllWindows()