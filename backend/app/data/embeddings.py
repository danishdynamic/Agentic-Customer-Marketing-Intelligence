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
    if not texts:
        return []

    # Wrap each string into types.Content to prevent Gemini from 
    # merging multiple texts into a single document embedding output
    formatted_contents = [
        types.Content(parts=[types.Part.from_text(text=text)])
        for text in texts
    ]

    result = client.models.embed_content(
        model=settings.gemini_embeddings,
        contents=formatted_contents,
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type="RETRIEVAL_DOCUMENT",
        ),
    )

    return [
        normalize_embedding(embedding.values)
        for embedding in result.embeddings
    ]


def generate_embedding(
    text: str,
    task_type: str = "RETRIEVAL_QUERY",
) -> list[float]:
    """
    Generates a normalized 1D embedding for a single search query.
    """
    result = client.models.embed_content(
        model=settings.gemini_embeddings,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768,
            task_type=task_type,
        ),
    )

    return normalize_embedding(result.embeddings[0].values)