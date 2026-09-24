import argparse

from sqlalchemy import select

from app.data.embeddings import generate_embeddings
from app.db.database import SessionLocal
from app.db.models import AdDocument


DEFAULT_LIMIT = 100
BATCH_SIZE = 20

"""
Ad 1 ─┐
Ad 2  │
Ad 3  │
...   ├──→ ONE embedding request
Ad 20 ┘

Ad 21 ─┐
Ad 22  │
...    ├──→ ONE embedding request
Ad 40  ┘
"""

def main(limit: int):
    db = SessionLocal()

    try:
        documents = db.scalars(
            select(AdDocument)
            .where(
                AdDocument.embedding.is_(None)
            )
            .limit(limit)
        ).all()

        total = len(documents)

        print(
            f"Documents selected: {total}"
        )

        for start in range(
            0,
            total,
            BATCH_SIZE,
        ):
            batch = documents[
                start:start + BATCH_SIZE
            ]

            texts = [
                document.content
                for document in batch
            ]

            print(
                f"Embedding batch "
                f"{start + 1}-{start + len(batch)} "
                f"of {total}"
            )

            embeddings = generate_embeddings(
                texts
            )

            for document, embedding in zip(
                batch,
                embeddings,
            ):
                document.embedding = embedding

            db.commit()

        print("Embedding generation complete.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
    )

    args = parser.parse_args()

    main(args.limit)


