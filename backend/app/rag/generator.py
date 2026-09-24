from google import genai
from google.genai import types

from app.core.config import get_settings


settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key
)


SYSTEM_INSTRUCTION = """
You are an advertising analytics assistant.

Answer questions using ONLY the provided advertising
data.

Do not invent metrics, ads, campaigns, or conclusions.

When numerical information is available, use the
provided numbers.

When discussing marketing messaging, refer to the
actual ad copy provided in the context.

If the provided context is insufficient to answer the
question, clearly say that the available data is
insufficient.

Keep answers concise and analytical.
"""


def generate_answer(
    question: str,
    context: str,
) -> str:

    prompt = f"""
{SYSTEM_INSTRUCTION}

USER QUESTION:
{question}

ADVERTISING DATA:
{context}

ANSWER:
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        ),
    )

    return response.text