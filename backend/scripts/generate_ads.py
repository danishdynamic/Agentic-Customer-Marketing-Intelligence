from sqlalchemy import select

from app.data.document_builder import build_ad_document
from app.data.generator import generate_ads
from app.db.database import SessionLocal
from app.db.models import Ad, AdDocument, Campaign


def main():
    number_of_ads = 1000

    print(f"Generating {number_of_ads} ads...")

    generated_ads = generate_ads(number_of_ads)

    db = SessionLocal()

    try:
        campaigns = {}

        for item in generated_ads:

            campaign_key = item["campaign_id"]

            if campaign_key not in campaigns:

                campaign = Campaign(
                    campaign_id=item["campaign_id"],
                    campaign_name=item["campaign_name"],
                    platform=item["platform"],
                )

                db.add(campaign)
                db.flush()

                campaigns[campaign_key] = campaign

            campaign = campaigns[campaign_key]

            ad = Ad(
                ad_id=item["ad_id"],
                campaign_id=campaign.id,
                platform=item["platform"],
                date=item["date"],
                impressions=item["impressions"],
                reach=item["reach"],
                clicks=item["clicks"],
                spend=item["spend"],
                conversions=item["conversions"],
                conversion_value=item["conversion_value"],
                ctr=item["ctr"],
                cpc=item["cpc"],
                cpa=item["cpa"],
                roas=item["roas"],
                audience=item["audience"],
                age_group=item["age_group"],
                gender=item["gender"],
                country=item["country"],
                device=item["device"],
                placement=item["placement"],
                headline=item["headline"],
                primary_text=item["primary_text"],
                description=item["description"],
                call_to_action=item["call_to_action"],
                marketing_angle=item["marketing_angle"],
                tone=item["tone"],
                offer_type=item["offer_type"],
                product_category=item["product_category"],
            )

            db.add(ad)
            db.flush()

            document = AdDocument(
                ad_id=ad.id,
                content=build_ad_document(ad),
            )

            db.add(document)

        db.commit()

        print("Ads successfully inserted.")
        print(f"Generated ads: {len(generated_ads)}")
        print(f"Campaigns: {len(campaigns)}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()