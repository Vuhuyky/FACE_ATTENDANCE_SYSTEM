import json
import numpy as np


def embedding_to_json(embedding):
    """
    numpy array -> json string
    """
    return json.dumps(
        embedding.tolist()
    )


def json_to_embedding(json_string):
    """
    json string -> numpy array
    """
    return np.array(
        json.loads(json_string)
    )


def cosine_similarity(e1, e2):

    e1 = e1 / np.linalg.norm(e1)

    e2 = e2 / np.linalg.norm(e2)

    return np.dot(e1, e2)

def find_best_match(
    current_embedding,
    students,
    threshold=0.5
):
    """
    students:
    [
        (student_code,
         full_name,
         embedding)
    ]
    """

    best_similarity = -1
    best_student = None

    for student in students:

        student_id = student[0]
        student_code = student[1]
        full_name = student[2]
        embedding = student[3]

        similarity = cosine_similarity(
            current_embedding,
            embedding
        )

        if similarity > best_similarity:

            best_similarity = similarity
            best_student = student

    if best_similarity < threshold:

        return None, best_similarity

    return best_student, best_similarity