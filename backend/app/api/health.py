from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():
    return {
        "status": "ok",
    }


@router.get("/db")
def database_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    vector_version = db.execute(
        text(
            """
            SELECT extversion
            FROM pg_extension
            WHERE extname = 'vector'
            """
        )
    ).scalar()

    return {
        "status": "ok",
        "database": "connected",
        "pgvector": vector_version,
    }