from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.rag.pipeline import answer_query


router = APIRouter(
    prefix="/api/v1/rag",
    tags=["RAG"],
)


class RAGQueryRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=1000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )


@router.post("/query")
def rag_query(
    request: RAGQueryRequest,
    db: Session = Depends(get_db),
):
    return answer_query(
        db=db,
        query=request.question,
        top_k=request.top_k,
    )