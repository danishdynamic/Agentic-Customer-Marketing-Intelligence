def classify_query(query: str) -> str:
    query_lower = query.lower()

    sql_signals = [
        "highest",
        "lowest",
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

    semantic_signals = [
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
        "characteristics",
    ]

    has_sql = any(
        signal in query_lower
        for signal in sql_signals
    )

    has_semantic = any(
        signal in query_lower
        for signal in semantic_signals
    )

    # Explicit semantic-only questions
    semantic_only_patterns = [
        "use urgency",
        "use premium",
        "use discount",
        "use social proof",
        "messaging",
        "messaging.",
        "language",
        "tone",
    ]

    if any(
        pattern in query_lower
        for pattern in semantic_only_patterns
    ) and not any(
        metric in query_lower
        for metric in [
            "roas",
            "ctr",
            "cpa",
            "spend",
            "conversions",
        ]
    ):
        return "vector"

    # Hybrid when structured constraints
    # and semantic requirements coexist.
    if has_sql and has_semantic:
        return "hybrid"

    if has_sql:
        return "sql"

    if has_semantic:
        return "vector"

    return "hybrid"