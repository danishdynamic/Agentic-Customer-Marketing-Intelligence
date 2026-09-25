from collections import defaultdict

from app.db.database import SessionLocal
from app.evaluation.dataset import EVALUATION_DATASET
from app.evaluation.retrieval import evaluate_case


def main():

    db = SessionLocal()

    results = []

    try:
        print("=" * 70)
        print("ADS RAG RETRIEVAL EVALUATION")
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

            result = evaluate_case(
                db=db,
                case=case,
                top_k=5,
            )

            results.append(result)

            print(
                f"Route: "
                f"{result['actual_route']} "
                f"({'✓' if result['route_correct'] else '✗'})"
            )

            print(
                f"Precision@5: "
                f"{result['precision']:.3f}"
            )

            print(
                f"Recall@5: "
                f"{result['recall']:.3f}"
            )

            print(
                f"Hit Rate@5: "
                f"{result['hit_rate']:.3f}"
            )

        print()
        print("=" * 70)
        print("OVERALL RESULTS")
        print("=" * 70)

        if not results:
            return

        avg_precision = sum(
            result["precision"]
            for result in results
        ) / len(results)

        avg_recall = sum(
            result["recall"]
            for result in results
        ) / len(results)

        avg_hit_rate = sum(
            result["hit_rate"]
            for result in results
        ) / len(results)

        route_accuracy = sum(
            result["route_correct"]
            for result in results
        ) / len(results)

        print(
            f"Precision@5: {avg_precision:.3f}"
        )

        print(
            f"Recall@5:    {avg_recall:.3f}"
        )

        print(
            f"Hit Rate@5:  {avg_hit_rate:.3f}"
        )

        print(
            f"Route Acc:   {route_accuracy:.3f}"
        )

        print()
        print("=" * 70)
        print("BY QUERY TYPE")
        print("=" * 70)

        grouped = defaultdict(list)

        for result in results:
            grouped[
                result["query_type"]
            ].append(result)

        for query_type, group in grouped.items():

            precision = sum(
                result["precision"]
                for result in group
            ) / len(group)

            recall = sum(
                result["recall"]
                for result in group
            ) / len(group)

            hit_rate = sum(
                result["hit_rate"]
                for result in group
            ) / len(group)

            print()
            print(query_type.upper())

            print(
                f"  Precision@5: {precision:.3f}"
            )

            print(
                f"  Recall@5:    {recall:.3f}"
            )

            print(
                f"  Hit Rate@5:  {hit_rate:.3f}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()