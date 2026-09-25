def precision_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    relevant_count = sum(
        1
        for ad_id in retrieved
        if ad_id in relevant_ids
    )

    return relevant_count / len(retrieved)


def recall_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    if not relevant_ids:
        return 0.0

    retrieved = retrieved_ids[:k]

    relevant_count = sum(
        1
        for ad_id in retrieved
        if ad_id in relevant_ids
    )

    return relevant_count / len(relevant_ids)


def hit_rate_at_k(
    retrieved_ids: list[str],
    relevant_ids: set[str],
    k: int,
) -> float:
    retrieved = retrieved_ids[:k]

    return float(
        any(
            ad_id in relevant_ids
            for ad_id in retrieved
        )
    )