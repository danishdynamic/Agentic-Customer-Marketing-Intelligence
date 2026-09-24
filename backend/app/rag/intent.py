import re


def extract_intent(query: str) -> dict:
    text = query.lower()

    intent = {
        "platform": None,
        "marketing_angle": None,
        "min_roas": None,
        "max_roas": None,
        "min_ctr": None,
        "max_cpa": None,
        "high_performing": False,
    }

    # --------------------------------------------------
    # Platform
    # --------------------------------------------------

    if "facebook" in text:
        intent["platform"] = "Facebook"

    elif "google" in text:
        intent["platform"] = "Google"

    # --------------------------------------------------
    # Marketing angle
    # --------------------------------------------------

    angles = [
        "discount",
        "urgency",
        "premium",
        "social proof",
        "convenience",
        "new arrival",
    ]

    for angle in angles:
        if angle in text:
            intent["marketing_angle"] = angle
            break

    # --------------------------------------------------
    # Explicit ROAS threshold
    # --------------------------------------------------

    roas_match = re.search(
        r"roas\s*(?:above|over|greater than|>)\s*(\d+(?:\.\d+)?)",
        text,
    )

    if roas_match:
        intent["min_roas"] = float(
            roas_match.group(1)
        )

    # --------------------------------------------------
    # Explicit CTR threshold
    # --------------------------------------------------

    ctr_match = re.search(
        r"ctr\s*(?:above|over|greater than|>)\s*(\d+(?:\.\d+)?)",
        text,
    )

    if ctr_match:
        value = float(ctr_match.group(1))

        # User might say "CTR above 5%"
        if "%" in ctr_match.group(0):
            value /= 100

        intent["min_ctr"] = value

    # --------------------------------------------------
    # Explicit CPA threshold
    # --------------------------------------------------

    cpa_match = re.search(
        r"cpa\s*(?:below|under|less than|<)\s*\$?(\d+(?:\.\d+)?)",
        text,
    )

    if cpa_match:
        intent["max_cpa"] = float(
            cpa_match.group(1)
        )

    # --------------------------------------------------
    # "High-performing"
    # --------------------------------------------------

    if any(
        phrase in text
        for phrase in [
            "high-performing",
            "high performing",
            "top performing",
            "best performing",
            "best ads",
        ]
    ):
        intent["high_performing"] = True

        # We deliberately don't use an arbitrary
        # percentile here. Instead, choose a
        # conservative business threshold.
        if intent["min_roas"] is None:
            intent["min_roas"] = 2.0

    return intent