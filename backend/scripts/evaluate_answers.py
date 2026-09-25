from app.db.database import SessionLocal
from app.evaluation.answer_evaluation import evaluate_answer
from app.evaluation.dataset import EVALUATION_DATASET


def main():
    db = SessionLocal()

    results = []

    try:
        print("=" * 70)
        print("ADS RAG ANSWER EVALUATION")
        print("=" * 70)

        for index, case in enumerate(
            EVALUATION_DATASET,
            start=1,
        ):
            print()
            print(
                f"[{index}/{len(EVALUATION_DATASET)}] "
                f"{case.question}"
            )

            result = evaluate_answer(
                db=db,
                question=case.question,
                top_k=5,
            )

            results.append(result)

            print(
                f"Route: {result['route']}"
            )

            print(
                f"Faithfulness: "
                f"{result['faithfulness']:.3f}"
            )

            print(
                f"Relevance:    "
                f"{result['relevance']:.3f}"
            )

            print(
                f"Completeness: "
                f"{result['completeness']:.3f}"
            )

            print(
                f"Reason: "
                f"{result['reason']}"
            )

        # --------------------------------
        # Overall results
        # --------------------------------

        if not results:
            return

        avg_faithfulness = sum(
            result["faithfulness"]
            for result in results
        ) / len(results)

        avg_relevance = sum(
            result["relevance"]
            for result in results
        ) / len(results)

        avg_completeness = sum(
            result["completeness"]
            for result in results
        ) / len(results)

        print()
        print("=" * 70)
        print("OVERALL RESULTS")
        print("=" * 70)

        print(
            f"Faithfulness: {avg_faithfulness:.3f}"
        )

        print(
            f"Relevance:    {avg_relevance:.3f}"
        )

        print(
            f"Completeness: {avg_completeness:.3f}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()