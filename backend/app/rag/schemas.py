from dataclasses import dataclass


@dataclass
class RetrievedDocument:
    source: str
    ad_id: str
    content: str
    score: float | None = None