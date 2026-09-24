import random
from datetime import date, timedelta
from decimal import Decimal

from faker import Faker


fake = Faker()

PLATFORMS = ["Facebook", "Google"]

COUNTRIES = [
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "India",
]

AGE_GROUPS = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55+",
]

GENDERS = [
    "All",
    "Female",
    "Male",
]

DEVICES = [
    "Mobile",
    "Desktop",
    "Tablet",
]

PLACEMENTS = [
    "Feed",
    "Stories",
    "Search",
    "Display",
    "Reels",
]

PRODUCT_CATEGORIES = [
    "Running Shoes",
    "Skincare",
    "Smartphones",
    "Fitness Equipment",
    "Coffee",
    "Travel Accessories",
    "Headphones",
    "Fashion",
]

MARKETING_ANGLES = [
    "Discount",
    "Urgency",
    "Premium",
    "Social Proof",
    "Convenience",
    "New Arrival",
]

TONES = [
    "Energetic",
    "Urgent",
    "Professional",
    "Friendly",
    "Premium",
    "Inspirational",
]

OFFER_TYPES = [
    "Percentage Discount",
    "Free Shipping",
    "Limited Time",
    "Bundle",
    "None",
]

CALL_TO_ACTIONS = [
    "Shop Now",
    "Learn More",
    "Buy Now",
    "Get Offer",
    "Sign Up",
]


def choose_campaign_name(product_category: str) -> str:
    campaign_templates = [
        f"{product_category} Summer Campaign",
        f"{product_category} Performance Campaign",
        f"{product_category} New Collection",
        f"{product_category} Growth Campaign",
        f"{product_category} Customer Acquisition",
    ]

    return random.choice(campaign_templates)


def generate_marketing_content(
    product_category: str,
    marketing_angle: str,
    offer_type: str,
):
    product = product_category.lower()

    if marketing_angle == "Discount":
        headline = random.choice([
            f"Save Big on {product_category}",
            f"Up to 30% Off {product_category}",
            f"Your {product_category} Deal Is Here",
        ])

        primary_text = random.choice([
            f"Upgrade your {product} today and save with our limited discount.",
            f"Get premium {product} without paying full price. Shop our latest offer.",
            f"Discover great {product} at a price you'll love.",
        ])

        description = "Limited savings available while the offer lasts."

    elif marketing_angle == "Urgency":
        headline = random.choice([
            f"Last Chance to Get {product_category}",
            f"Don't Miss This {product_category} Deal",
            f"Only a Few Days Left",
        ])

        primary_text = random.choice([
            f"Time is running out. Grab your {product} before this offer ends.",
            f"Don't wait. This special {product} offer is available for a limited time.",
            f"Your chance to save on {product} ends soon.",
        ])

        description = "Limited-time offer. Act before it's gone."

    elif marketing_angle == "Premium":
        headline = random.choice([
            f"Experience Premium {product_category}",
            f"Elevate Your Everyday with {product_category}",
            f"Designed for Those Who Expect More",
        ])

        primary_text = random.choice([
            f"Discover carefully crafted {product} designed for customers who value quality.",
            f"Experience exceptional materials, thoughtful design, and premium performance.",
            f"Upgrade your lifestyle with premium {product} built for lasting quality.",
        ])

        description = "Premium quality designed for a better everyday experience."

    elif marketing_angle == "Social Proof":
        headline = random.choice([
            f"Thousands Love Our {product_category}",
            f"See Why Customers Choose Us",
            f"A Customer Favorite",
        ])

        primary_text = random.choice([
            f"Join thousands of customers who already love our {product}.",
            f"See why customers keep coming back for our {product}.",
            f"Discover one of our most-loved {product} products.",
        ])

        description = "Loved by customers around the world."

    elif marketing_angle == "Convenience":
        headline = random.choice([
            f"Make Life Easier with {product_category}",
            f"{product_category} Made Simple",
            f"Simple. Convenient. Ready for You.",
        ])

        primary_text = random.choice([
            f"Get the {product} you need without the hassle.",
            f"Simple shopping, fast delivery, and products designed around you.",
            f"Everything you need in one convenient place.",
        ])

        description = "Easy shopping and convenient delivery."

    else:
        headline = random.choice([
            f"Meet Our New {product_category}",
            f"Introducing {product_category}",
            f"Discover What's New",
        ])

        primary_text = random.choice([
            f"Discover our newest {product} collection.",
            f"Meet the latest addition to our product range.",
            f"Something new has arrived. Explore our latest {product}.",
        ])

        description = "Discover the latest products from our collection."

    return headline, primary_text, description


def calculate_performance(
    marketing_angle: str,
    platform: str,
):
    """
    Creates realistic relationships between marketing strategy
    and advertising performance.

    These are tendencies, not deterministic rules.
    """

    base_ctr = {
        "Discount": 0.035,
        "Urgency": 0.040,
        "Premium": 0.022,
        "Social Proof": 0.032,
        "Convenience": 0.029,
        "New Arrival": 0.027,
    }[marketing_angle]

    platform_adjustment = {
        "Facebook": 1.05,
        "Google": 0.95,
    }[platform]

    ctr = base_ctr * platform_adjustment
    ctr *= random.uniform(0.75, 1.25)

    impressions = random.randint(10_000, 150_000)

    clicks = max(
        1,
        int(impressions * ctr),
    )

    spend = random.uniform(500, 10_000)

    cpc = spend / clicks

    # Conversion rate also varies by marketing angle.
    conversion_rate = {
        "Discount": 0.075,
        "Urgency": 0.080,
        "Premium": 0.055,
        "Social Proof": 0.070,
        "Convenience": 0.065,
        "New Arrival": 0.060,
    }[marketing_angle]

    conversion_rate *= random.uniform(0.70, 1.30)

    conversions = max(
        1,
        int(clicks * conversion_rate),
    )

    average_order_value = random.uniform(40, 180)

    conversion_value = conversions * average_order_value

    cpa = spend / conversions
    roas = conversion_value / spend

    return {
        "impressions": impressions,
        "clicks": clicks,
        "spend": round(spend, 2),
        "conversions": conversions,
        "conversion_value": round(conversion_value, 2),
        "ctr": round(clicks / impressions, 4),
        "cpc": round(cpc, 4),
        "cpa": round(cpa, 4),
        "roas": round(roas, 4),
    }


def generate_ad(
    ad_number: int,
    campaign_number: int,
):
    platform = random.choice(PLATFORMS)

    product_category = random.choice(PRODUCT_CATEGORIES)
    marketing_angle = random.choice(MARKETING_ANGLES)
    offer_type = random.choice(OFFER_TYPES)

    campaign_name = choose_campaign_name(
        product_category
    )

    headline, primary_text, description = generate_marketing_content(
        product_category,
        marketing_angle,
        offer_type,
    )

    performance = calculate_performance(
        marketing_angle,
        platform,
    )

    start_date = date(2026, 1, 1)

    ad_date = start_date + timedelta(
        days=random.randint(0, 180)
    )

    impressions = performance["impressions"]

    reach = int(
        impressions * random.uniform(0.65, 0.90)
    )

    return {
        "campaign_id": f"CAMP_{campaign_number:04d}",
        "campaign_name": campaign_name,
        "platform": platform,

        "ad_id": f"{platform[:2].upper()}_{ad_number:05d}",

        "date": ad_date,

        "impressions": impressions,
        "reach": reach,
        "clicks": performance["clicks"],
        "spend": Decimal(str(performance["spend"])),
        "conversions": performance["conversions"],
        "conversion_value": Decimal(
            str(performance["conversion_value"])
        ),
        "ctr": Decimal(str(performance["ctr"])),
        "cpc": Decimal(str(performance["cpc"])),
        "cpa": Decimal(str(performance["cpa"])),
        "roas": Decimal(str(performance["roas"])),

        "audience": f"{product_category} enthusiasts",
        "age_group": random.choice(AGE_GROUPS),
        "gender": random.choice(GENDERS),
        "country": random.choice(COUNTRIES),
        "device": random.choice(DEVICES),
        "placement": random.choice(PLACEMENTS),

        "headline": headline,
        "primary_text": primary_text,
        "description": description,

        "call_to_action": random.choice(
            CALL_TO_ACTIONS
        ),

        "marketing_angle": marketing_angle,
        "tone": random.choice(TONES),
        "offer_type": offer_type,
        "product_category": product_category,
    }


def generate_ads(
    number_of_ads: int = 1000,
):
    ads = []

    for i in range(1, number_of_ads + 1):
        campaign_number = ((i - 1) // 20) + 1

        ads.append(
            generate_ad(
                ad_number=i,
                campaign_number=campaign_number,
            )
        )

    return ads