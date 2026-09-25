from app.db.database import SessionLocal
from app.evaluation.dataset import EVALUATION_DATASET
from app.evaluation.ground_truth import get_relevant_ad_ids


def main():
    db = SessionLocal()

    try:
        for case in EVALUATION_DATASET:
            relevant_ids = get_relevant_ad_ids(
                db,
                case,
            )

            print()
            print(case.question)
            print(f"Type: {case.query_type}")
            print(f"Relevant ads: {len(relevant_ids)}")

            if relevant_ids:
                print(
                    f"Example IDs: "
                    f"{list(relevant_ids)[:5]}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()