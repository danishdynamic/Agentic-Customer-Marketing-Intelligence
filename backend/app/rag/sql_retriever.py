import re

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.db.models import Ad


def highest_roas(
    db: Session,
    platform: str | None = None,
    top_k: int = 5,
):
    statement: Select = select(Ad)

    if platform:
        statement = statement.where(
            Ad.platform.ilike(platform)
        )

    statement = (
        statement
        .order_by(Ad.roas.desc())
        .limit(top_k)
    )

    return db.scalars(statement).all()


def lowest_cpa(
    db: Session,
    platform: str | None = None,
    top_k: int = 5,
):
    statement: Select = select(Ad)

    if platform:
        statement = statement.where(
            Ad.platform.ilike(platform)
        )

    statement = (
        statement
        .order_by(Ad.cpa.asc())
        .limit(top_k)
    )

    return db.scalars(statement).all()


def average_performance_by_angle(db: Session):
    statement = (
        select(
            Ad.marketing_angle,
            func.count(Ad.id).label("ad_count"),
            func.avg(Ad.ctr).label("avg_ctr"),
            func.avg(Ad.roas).label("avg_roas"),
            func.avg(Ad.cpa).label("avg_cpa"),
        )
        .group_by(Ad.marketing_angle)
        .order_by(func.avg(Ad.roas).desc())
    )

    return db.execute(statement).all()


def filtered_ads(
    db: Session,
    platform: str | None = None,
    marketing_angle: str | None = None,
    min_roas: float | None = None,
    max_roas: float | None = None,
    min_ctr: float | None = None,
    max_cpa: float | None = None,
    top_k: int = 20,
):
    """
    Structured filtering for hybrid queries.
    """

    statement: Select = select(Ad)

    if platform:
        statement = statement.where(
            Ad.platform.ilike(platform)
        )

    if marketing_angle:
        statement = statement.where(
            Ad.marketing_angle.ilike(
                marketing_angle
            )
        )

    if min_roas is not None:
        statement = statement.where(
            Ad.roas >= min_roas
        )

    if max_roas is not None:
        statement = statement.where(
            Ad.roas <= max_roas
        )

    if min_ctr is not None:
        statement = statement.where(
            Ad.ctr >= min_ctr
        )

    if max_cpa is not None:
        statement = statement.where(
            Ad.cpa <= max_cpa
        )

    statement = (
        statement
        .order_by(Ad.roas.desc())
        .limit(top_k)
    )

    return db.scalars(statement).all()


def retrieve_sql(
    db: Session,
    query: str,
    intent: dict,
    top_k: int = 5,
):
    query_lower = query.lower()

    # -------------------------
    # Highest ROAS
    # -------------------------

    if "highest roas" in query_lower:
        return highest_roas(
            db=db,
            platform=intent.get("platform"),
            top_k=top_k,
        )

    # -------------------------
    # Lowest CPA
    # -------------------------

    if "lowest cpa" in query_lower:
        return lowest_cpa(
            db=db,
            platform=intent.get("platform"),
            top_k=top_k,
        )

    # -------------------------
    # Filtered SQL retrieval
    # -------------------------

    return filtered_ads(
        db=db,
        platform=intent.get("platform"),
        marketing_angle=intent.get("marketing_angle"),
        min_roas=intent.get("min_roas"),
        max_roas=intent.get("max_roas"),
        min_ctr=intent.get("min_ctr"),
        max_cpa=intent.get("max_cpa"),
        top_k=top_k,
    )