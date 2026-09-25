import json

from google import genai
from google.genai import types

from app.core.config import get_settings


settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key
)


JUDGE_INSTRUCTION = """
You are an evaluator for an advertising analytics RAG system.

Evaluate the generated answer using ONLY the provided
question, retrieved context, and answer.

Do not evaluate whether the underlying advertising strategy
is good or bad.

Score each dimension from 0.0 to 1.0:

faithfulness:
How well is the answer supported by the retrieved context?
Penalize invented facts, metrics, ads, or unsupported claims.

relevance:
How directly does the answer address the user's question?

completeness:
Does the answer address the important parts of the question
that can be answered from the provided context?

Return ONLY valid JSON with this structure:

{
  "faithfulness": 0.0,
  "relevance": 0.0,
  "completeness": 0.0,
  "reason": "short explanation"
}
"""


def judge_answer(
    question: str,
    context: str,
    answer: str,
) -> dict:

    prompt = f"""
{JUDGE_INSTRUCTION}

QUESTION:
{question}

RETRIEVED CONTEXT:
{context}

GENERATED ANSWER:
{answer}

EVALUATION:
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
        ),
    )

    return json.loads(response.text)