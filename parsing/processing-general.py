import logging

from constants import DATA_TYPES, FIRST_DATE, NUMBER_OF_DATES, PARTIES
from models import Ad
from utils import recursive_round, render_template

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


if __name__ == "__main__":

    ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))
    ads_per_party = {p: [ad for ad in ads if ad.party == p] for p in PARTIES}

    most_expensive_ad = max(ads, key=lambda e: e.average_spending_per_day)

    logging.info("Creating general data.")

    general_data = {
        "number-of-ads-total": len(ads),
        "number-of-ads-party": [len(ads_per_party[p]) for p in PARTIES],
        "spending-total-lower": sum(ad.spending_lower for ad in ads),
        "spending-total-upper": sum(ad.spending_upper for ad in ads),
        "spending-party": [
            sum(ad.average_spending for ad in ads_per_party[p]) for p in PARTIES
        ],
        "impressions-party": [
            sum(ad.average_impressions for ad in ads_per_party[p]) for p in PARTIES
        ],
        "most-expensive-ad": {
            "id": most_expensive_ad.ad_id,
            "party": most_expensive_ad.party,
            "spend-per-day": most_expensive_ad.average_spending_per_day,
            "days": most_expensive_ad.days_active,
        },
        "number-of-ads-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "spending-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "impressions-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "estimated-audience-size-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
    }

    logging.info("Creating party specific data.")

    for party_i, party in enumerate(PARTIES):
        for ad in ads_per_party[party]:
            for date_i in ad.active_date_indices():
                for data_type in DATA_TYPES:
                    general_data[f"{data_type}-party-daily"][party_i][
                        date_i
                    ] += ad.rank_to_data(data_type, "total", per_day=True)

    logging.info("Writing templates.")

    logging.debug("Writing index.html.")
    recursive_round(general_data)
    render_template("index.html", "index.html", general_data=general_data)

    logging.debug("Writing about.html.")
    render_template("about.html", "about.html")
