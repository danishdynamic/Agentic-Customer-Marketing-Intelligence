from sqlalchemy.orm import Session

from app.evaluation.ground_truth import get_relevant_ad_ids
from app.evaluation.metrics import (
    hit_rate_at_k,
    precision_at_k,
    recall_at_k,
)
from app.evaluation.schemas import EvaluationCase
from app.rag.intent import extract_intent
from app.rag.router import classify_query
from app.rag.sql_retriever import retrieve_sql
from app.rag.vector_retriever import vector_search


def get_retrieved_ad_ids(
    db: Session,
    case: EvaluationCase,
    top_k: int = 5,
) -> tuple[str, list[str]]:

    route = classify_query(case.question)
    intent = extract_intent(case.question)

    retrieved_ids: list[str] = []

    # -------------------------
    # SQL
    # -------------------------

    if route == "sql":
        results = retrieve_sql(
            db=db,
            query=case.question,
            intent=intent,
            top_k=top_k,
        )

        retrieved_ids = [
            result.ad_id
            for result in results
        ]

    # -------------------------
    # Vector
    # -------------------------

    elif route == "vector":
        results = vector_search(
            db=db,
            query=case.question,
            top_k=top_k,
        )

        retrieved_ids = [
            ad.ad_id
            for ad, document, distance in results
        ]

    # -------------------------
    # Hybrid
    # -------------------------

    elif route == "hybrid":
        sql_results = retrieve_sql(
            db=db,
            query=case.question,
            intent=intent,
            top_k=top_k,
        )

        vector_results = vector_search(
            db=db,
            query=case.question,
            top_k=top_k,
        )

        sql_ids = [
            result.ad_id
            for result in sql_results
        ]

        vector_ids = [
            ad.ad_id
            for ad, document, distance in vector_results
        ]

        # Preserve SQL ranking first, then add semantic results.
        combined_ids = []

        for ad_id in sql_ids + vector_ids:
            if ad_id not in combined_ids:
                combined_ids.append(ad_id)

        retrieved_ids = combined_ids[:top_k]

    else:
        raise ValueError(
            f"Unsupported route: {route}"
        )

    return route, retrieved_ids


def evaluate_case(
    db: Session,
    case: EvaluationCase,
    top_k: int = 5,
) -> dict:

    route, retrieved_ids = get_retrieved_ad_ids(
        db=db,
        case=case,
        top_k=top_k,
    )

    relevant_ids = get_relevant_ad_ids(
        db=db,
        case=case,
    )

    return {
        "question": case.question,
        "query_type": case.query_type,
        "expected_route": case.expected_route,
        "actual_route": route,
        "route_correct": route == case.expected_route,
        "relevant_count": len(relevant_ids),
        "retrieved_ids": retrieved_ids,
        "precision": precision_at_k(
            retrieved_ids,
            relevant_ids,
            top_k,
        ),
        "recall": recall_at_k(
            retrieved_ids,
            relevant_ids,
            top_k,
        ),
        "hit_rate": hit_rate_at_k(
            retrieved_ids,
            relevant_ids,
            top_k,
        ),
    }