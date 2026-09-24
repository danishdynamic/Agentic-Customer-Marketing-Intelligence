def classify_query(query: str) -> str:
    query_lower = query.lower()

    sql_keywords = [
        "highest",
        "lowest",
        "best",
        "worst",
        "average",
        "total",
        "count",
        "roas",
        "ctr",
        "cpc",
        "cpa",
        "spend",
        "conversions",
        "impressions",
        "clicks",
        "platform",
    ]

    semantic_keywords = [
        "message",
        "messaging",
        "headline",
        "copy",
        "tone",
        "urgency",
        "premium",
        "discount",
        "creative",
        "language",
        "theme",
        "themes",
        "positioning",
    ]

    has_sql = any(
        keyword in query_lower
        for keyword in sql_keywords
    )

    has_semantic = any(
        keyword in query_lower
        for keyword in semantic_keywords
    )

    if has_sql and has_semantic:
        return "hybrid"

    if has_sql:
        return "sql"

    if has_semantic:
        return "vector"

    return "hybrid"