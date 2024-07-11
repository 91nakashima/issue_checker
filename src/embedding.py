from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


def get_embedding(text) -> list[float]:
    model = 'text-embedding-3-small'
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def find_embeddings(
    base_embeddings: list[float],
    compare_embeddings: list[list[float]],
    ids: list[int],
    threshold: float
) -> list[dict[int, float]]:
    """
    Params
    ---
    base_embeddings: list[float]
        The embeddings of the base text

    compare_embeddings: list[list[float]]
        The embeddings of the texts to compare

    threshold: float
        The threshold to compare the embeddings

    Returns
    ---
    list[dict[int, float]]
        The list of ids of the texts that are similar to the base text
    """

    similar_ids: dict[int, float] = []
    for i, compare_embedding in enumerate(compare_embeddings):
        # not working
        # similarity = client.embeddings.similarity(base_embeddings, compare_embedding).data[0].score
        # if similarity > threshold:
        #     similar_ids.append(ids[i])

        similarity = sum([a * b for a, b in zip(base_embeddings, compare_embedding)])
        if similarity > threshold:
            similar_ids.append({
                "val": similarity,
                "id": ids[i]
            })

    # おおきい順にソート
    similar_ids = sorted(similar_ids, key=lambda x: x["val"], reverse=True)

    return similar_ids
