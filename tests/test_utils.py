import numpy as np

from utils import (
    embedding_to_json,
    json_to_embedding,
    cosine_similarity
)

e1 = np.array(
    [1, 2, 3]
)

json_data = embedding_to_json(e1)

print(json_data)

e2 = json_to_embedding(
    json_data
)

print(e2)

sim = cosine_similarity(
    e1,
    e2
)

print(sim)