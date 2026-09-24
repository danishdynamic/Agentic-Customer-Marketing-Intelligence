def build_ad_document(ad) -> str:
    """
    Converts an Ad ORM object or dictionary into a
    human-readable document for semantic retrieval.
    """

    return f"""
{ad.platform} Advertisement

Ad ID: {ad.ad_id}
Campaign: {ad.campaign.campaign_name}
Date: {ad.date}

TARGETING
Audience: {ad.audience}
Age Group: {ad.age_group}
Gender: {ad.gender}
Country: {ad.country}
Device: {ad.device}
Placement: {ad.placement}

PRODUCT
Category: {ad.product_category}

MARKETING
Marketing Angle: {ad.marketing_angle}
Tone: {ad.tone}
Offer Type: {ad.offer_type}
Call To Action: {ad.call_to_action}

HEADLINE
{ad.headline}

PRIMARY TEXT
{ad.primary_text}

DESCRIPTION
{ad.description}

PERFORMANCE
Impressions: {ad.impressions}
Reach: {ad.reach}
Clicks: {ad.clicks}
Spend: ${ad.spend}
Conversions: {ad.conversions}
Conversion Value: ${ad.conversion_value}
CTR: {ad.ctr}
CPC: ${ad.cpc}
CPA: ${ad.cpa}
ROAS: {ad.roas}
""".strip()