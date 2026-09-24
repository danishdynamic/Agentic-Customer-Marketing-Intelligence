from app.db.database import SessionLocal
from app.rag.pipeline import answer_query


QUERIES = [
    "Which ad had the highest ROAS?",
    "What ads use urgency messaging?",
    "What is the average ROAS by marketing angle?",
]


def main():

    db = SessionLocal()

    try:

        for query in QUERIES:

            print("\n")
            print("=" * 100)
            print(query)
            print("=" * 100)

            result = answer_query(
                db=db,
                query=query,
                top_k=5,
            )

            print("\nROUTE:")
            print(result["route"])

            print("\nANSWER:")
            print(result["answer"])

    finally:
        db.close()


if __name__ == "__main__":
    main()