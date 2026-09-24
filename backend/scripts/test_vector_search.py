from app.db.database import SessionLocal
from app.rag.vector_retriever import vector_search


def main():

    query = "ads using urgency and limited time messaging"

    db = SessionLocal()

    try:
        results = vector_search(
            db=db,
            query=query,
            top_k=5,
        )

        print("\nQUERY:")
        print(query)

        print("\nTOP RESULTS:\n")

        for document, distance in results:

            print("=" * 80)

            print(
                f"Document ID: {document.id}"
            )

            print(
                f"Distance: {distance:.4f}"
            )

            print()

            print(
                document.content[:1000]
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()