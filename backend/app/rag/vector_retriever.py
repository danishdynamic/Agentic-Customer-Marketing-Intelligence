from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.embeddings import generate_embedding
from app.db.models import Ad, AdDocument


def vector_search(
    db: Session,
    query: str,
    top_k: int = 5,
):
    # Use generate_embedding for a single string to get a 1D list[float]
    query_embedding = generate_embedding(query)

    # Defensive check: unwrap if it's accidentally wrapped in an outer list
    if (
        isinstance(query_embedding, list)
        and len(query_embedding) > 0
        and isinstance(query_embedding[0], list)
    ):
        query_embedding = query_embedding[0]

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