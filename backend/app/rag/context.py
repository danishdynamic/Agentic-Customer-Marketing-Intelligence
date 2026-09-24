from app.db.models import Ad


def ad_to_context(ad: Ad) -> str:
    return f"""
Ad ID: {ad.ad_id}
Platform: {ad.platform}
Campaign: {ad.campaign.campaign_name}
Date: {ad.date}

Product Category: {ad.product_category}

Marketing Angle: {ad.marketing_angle}
Tone: {ad.tone}
Offer Type: {ad.offer_type}

Headline: {ad.headline}

Primary Text:
{ad.primary_text}

Description:
{ad.description}

Performance:
Impressions: {ad.impressions}
Clicks: {ad.clicks}
Conversions: {ad.conversions}
Spend: ${ad.spend}
CTR: {ad.ctr}
CPC: ${ad.cpc}
CPA: ${ad.cpa}
ROAS: {ad.roas}
""".strip()