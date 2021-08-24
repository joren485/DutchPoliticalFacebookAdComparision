import logging

from constants import (
    FIRST_DATE,
    NUMBER_OF_DATES,
    PARTIES,
)

from models import Ad

from utils import recursive_round, render_template

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


if __name__ == "__main__":

    ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))
    ads_per_party = {p: [ad for ad in ads if ad.party == p] for p in PARTIES}

    most_expensive_ad = max(ads, key=lambda e: e.average_spending_per_day)

    LOGGER.info("Creating general data.")

    general_data = {
        "ads-total": len(ads),
        "ads-party": [len(ads_per_party[p]) for p in PARTIES],
        "spending-total-lower": sum(ad.spending_lower for ad in ads),
        "spending-total-upper": sum(ad.spending_upper for ad in ads),
        "spending-party": [
            sum(ad.spending_average for ad in ads_per_party[p]) for p in PARTIES
        ],
        "impressions-party": [
            sum(ad.impressions_average for ad in ads_per_party[p]) for p in PARTIES
        ],
        "most-expensive-ad": {
            "id": most_expensive_ad.ad_id,
            "party": most_expensive_ad.party,
            "spend-per-day": most_expensive_ad.average_spending_per_day,
            "days": most_expensive_ad.days_active,
        },
        "ads-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "spending-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "impressions-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "potential-reach-party-daily": [[0] * NUMBER_OF_DATES for _ in PARTIES],
    }

    LOGGER.info("Creating party specific data.")

    for party_i, party in enumerate(PARTIES):
        for ad in ads_per_party[party]:
            for date_i in ad.active_date_indices():

                general_data["ads-party-daily"][party_i][date_i] += 1
                general_data["spending-party-daily"][party_i][
                    date_i
                ] += ad.average_spending_per_day
                general_data["impressions-party-daily"][party_i][
                    date_i
                ] += ad.average_impressions_per_day
                general_data["potential-reach-party-daily"][party_i][
                    date_i
                ] += ad.average_potential_reach_per_day

    logging.info("Writing templates")

    logging.debug("Writing index.html")
    recursive_round(general_data)
    render_template("index.html", "index.html", general_data=general_data)

    logging.debug("Writing about.html")
    render_template("about.html", "about.html")
