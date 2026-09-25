from sqlalchemy.orm import Session

from app.rag.context import ad_to_context
from app.rag.generator import generate_answer
from app.rag.intent import extract_intent
from app.rag.router import classify_query
from app.rag.sql_retriever import (
    average_performance_by_angle,
    filtered_ads,
    highest_roas,
    lowest_cpa,
)
from app.rag.vector_retriever import vector_search


def deduplicate_results(results: dict) -> dict:
    sql_ad_ids = set()

    for item in results["sql_results"]:
        if isinstance(item, str):
            marker = "Ad ID: "
            if marker in item:
                ad_id = item.split(marker)[1].split("\n")[0]
                sql_ad_ids.add(ad_id)

    results["vector_results"] = [
        item
        for item in results["vector_results"]
        if item["ad_id"] not in sql_ad_ids
    ]

    return results


def retrieve(
    db: Session,
    query: str,
    top_k: int = 5,
):
    route = classify_query(query)
    intent = extract_intent(query)

    results = {
        "route": route,
        "intent": intent,
        "sql_results": [],
        "vector_results": [],
    }

    # --------------------------------------------------
    # SQL
    # --------------------------------------------------

    if route in {"sql", "hybrid"}:
        query_lower = query.lower()

        if "highest" in query_lower and "roas" in query_lower:
            ads = highest_roas(
                db=db,
                platform=intent["platform"],
                top_k=top_k,
            )
            results["sql_results"] = [ad_to_context(ad) for ad in ads]

        elif "lowest" in query_lower and "cpa" in query_lower:
            ads = lowest_cpa(
                db=db,
                platform=intent["platform"],
                top_k=top_k,
            )
            results["sql_results"] = [ad_to_context(ad) for ad in ads]

        elif "average" in query_lower:
            rows = average_performance_by_angle(db)
            results["sql_results"] = [
                {
                    "marketing_angle": row.marketing_angle,
                    "ad_count": row.ad_count,
                    "avg_ctr": float(row.avg_ctr),
                    "avg_roas": float(row.avg_roas),
                    "avg_cpa": float(row.avg_cpa),
                }
                for row in rows
            ]

        else:
            ads = filtered_ads(
                db=db,
                platform=intent["platform"],
                marketing_angle=intent["marketing_angle"],
                min_roas=intent["min_roas"],
                max_roas=intent["max_roas"],
                min_ctr=intent["min_ctr"],
                max_cpa=intent["max_cpa"],
                top_k=top_k * 3,
            )
            results["sql_results"] = [ad_to_context(ad) for ad in ads]

    # --------------------------------------------------
    # Vector search
    # --------------------------------------------------

    if route in {"vector", "hybrid"}:
        vector_results = vector_search(
            db=db,
            query=query,
            top_k=top_k,
        )

        results["vector_results"] = [
            {
                "ad_id": ad.ad_id,
                "distance": float(distance),
                "content": document.content,
            }
            for ad, document, distance in vector_results
        ]

    return results


def build_context(results: dict) -> str:
    sections = []

    if results["sql_results"]:
        sections.append(
            "STRUCTURED SQL RESULTS:\n" + str(results["sql_results"])
        )

    if results["vector_results"]:
        sections.append(
            "SEMANTIC SEARCH RESULTS:\n"
            + "\n\n".join(
                item["content"] for item in results["vector_results"]
            )
        )

    return "\n\n".join(sections)


def answer_query(
    db: Session,
    query: str,
    top_k: int = 5,
):
    retrieval = retrieve(
        db=db,
        query=query,
        top_k=top_k,
    )
    retrieval = deduplicate_results(retrieval)

    context = build_context(retrieval)

    answer = generate_answer(
        question=query,
        context=context,
    )

    return {
        "question": query,
        "route": retrieval["route"],
        "intent": retrieval["intent"],
        "answer": answer,
        "retrieval": retrieval,
        "context": context,
    }