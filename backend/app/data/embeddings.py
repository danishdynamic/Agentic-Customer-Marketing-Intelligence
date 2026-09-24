import numpy as np

from google import genai
from google.genai import types

from app.core.config import get_settings


settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key
)


def normalize_embedding(
    values: list[float],
) -> list[float]:

    vector = np.array(
        values,
        dtype=np.float32,
    )

    norm = np.linalg.norm(vector)

    if norm == 0:
        return values

    return (
        vector / norm
    ).tolist()


def generate_embeddings(
    texts: list[str],
) -> list[list[float]]:

    result = client.models.embed_content(
        model=settings.gemini_embeddings,
        contents=texts,
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type="RETRIEVAL_DOCUMENT",
        ),
    )

    return [
        normalize_embedding(
            embedding.values
        )
        for embedding in result.embeddings
    ]