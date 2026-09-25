from pydantic import BaseModel


class EvaluationCase(BaseModel):
    question: str
    query_type: str

    expected_route: str

    expected_ad_ids: list[str] = []

    expected_keywords: list[str] = []

    reference_answer: str | None = None