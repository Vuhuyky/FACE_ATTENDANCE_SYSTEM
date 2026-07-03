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
        (student_id, student_code, full_name,
         ..., embedding)
    ]

    NOTE: `embedding` is always read from the LAST
    position of the tuple (student[-1]), not a fixed
    index, so this keeps working no matter how many
    extra descriptive fields (course, section, room,
    photo_path, ...) get added in between.
    """

    best_similarity = -1
    best_student = None

    for student in students:

        embedding = student[-1]

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