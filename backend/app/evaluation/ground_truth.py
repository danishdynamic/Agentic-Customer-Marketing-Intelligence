from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models import Ad
from app.evaluation.schemas import EvaluationCase


def get_relevant_ad_ids(
    db: Session,
    case: EvaluationCase,
) -> set[str]:

    question = case.question.lower()

    # -------------------------
    # Highest ROAS
    # -------------------------

    if "highest roas" in question:
        max_roas = db.scalar(
            select(func.max(Ad.roas))
        )

        ads = db.scalars(
            select(Ad).where(
                Ad.roas == max_roas
            )
        ).all()

        return {
            ad.ad_id
            for ad in ads
        }

    # -------------------------
    # Lowest CPA
    # -------------------------

    if "lowest cpa" in question:
        min_cpa = db.scalar(
            select(func.min(Ad.cpa))
        )

        ads = db.scalars(
            select(Ad).where(
                Ad.cpa == min_cpa
            )
        ).all()

        return {
            ad.ad_id
            for ad in ads
        }

    # -------------------------
    # Generic filtering
    # -------------------------

    statement = select(Ad)

    # Platform
    if "facebook" in question:
        statement = statement.where(
            Ad.platform == "Facebook"
        )

    elif "google" in question:
        statement = statement.where(
            Ad.platform == "Google"
        )

    # Marketing angle
    angle_mapping = {
        "urgency": "Urgency",
        "premium": "Premium",
        "discount": "Discount",
        "social proof": "Social Proof",
        "convenience": "Convenience",
        "new arrival": "New Arrival",
    }

    for keyword, angle in angle_mapping.items():
        if keyword in question:
            statement = statement.where(
                Ad.marketing_angle == angle
            )
            break

    # High-performing
    if "high-performing" in question:
        statement = statement.where(
            Ad.roas >= 2.0
        )

    # Explicit ROAS
    if "roas above 2" in question:
        statement = statement.where(
            Ad.roas > 2.0
        )

    ads = db.scalars(statement).all()

    return {
        ad.ad_id
        for ad in ads
    }