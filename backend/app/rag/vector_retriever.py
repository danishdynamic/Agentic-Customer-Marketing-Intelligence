from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.embeddings import generate_embedding
from app.db.models import Ad, AdDocument


def vector_search(
    db: Session,
    query: str,
    top_k: int = 5,
):
    query_embedding = generate_embedding(query)

    distance = AdDocument.embedding.cosine_distance(
        query_embedding
    )

    statement = (
        select(
            Ad,
            AdDocument,
            distance.label("distance"),
        )
        .join(
            AdDocument,
            AdDocument.ad_id == Ad.id,
        )
        .where(
            AdDocument.embedding.is_not(None)
        )
        .order_by(distance)
        .limit(top_k)
    )

    return db.execute(statement).all()