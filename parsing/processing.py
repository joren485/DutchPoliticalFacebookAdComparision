import json
import logging
from datetime import datetime
from typing import Union

from constants import (
    AGE_RANGES,
    DATETIME_FORMAT,
    FIRST_DATE,
    GENDERS,
    NUMBER_OF_DATES,
    PARTIES,
    REGIONS,
)

from models import Ad

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def recursive_round(o: Union[dict, list], precision: int = 0):
    """
    Traverses an object recursively and rounds numbers found in lists.

    :param o: Object to round recursively.
    :param precision: Precision to use when rounding
    """
    if isinstance(o, dict):
        for key in o:
            recursive_round(o[key], 2 if "spend" in key else precision)
    elif isinstance(o, list) and len(o) > 0 and isinstance(o[0], (list, dict)):
        for object_element in o:
            recursive_round(object_element, precision)
    elif isinstance(o, list) and len(o) > 0 and isinstance(o[0], (int, float)):
        for object_index, object_element in enumerate(o):
            o[object_index] = round(object_element, precision)


if __name__ == '__main__':

    ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))
    ads_per_party = {p: [ad for ad in ads if ad.party == p] for p in PARTIES}

    most_expensive_ad = max(ads, key=lambda e: e.average_spending_per_day)

    LOGGER.info(f"Creating general data.")

    general_data = {
        "last-updated": datetime.now().strftime("%H:%M %d-%m-%Y"),
        "start-date": FIRST_DATE.strftime(DATETIME_FORMAT),
        "ads-total": len(ads),
        "ads-without-potential-reach": sum(1 for a in ads if not a.has_potential_reach),
        "ads-per-party": [len(ads_per_party[p]) for p in PARTIES],
        "spending-total-lower": sum(ad.spending_lower for ad in ads),
        "spending-total-upper": sum(ad.spending_upper for ad in ads),
        "spending-per-party": [sum(ad.spending_average for ad in ads_per_party[p]) for p in PARTIES],
        "impressions-per-party": [sum(ad.impressions_average for ad in ads_per_party[p]) for p in PARTIES],
        "most-expensive-ad": {
            "id": most_expensive_ad.ad_id,
            "party": most_expensive_ad.party,
            "spend-per-day": most_expensive_ad.average_spending_per_day,
            "days": most_expensive_ad.days_active,
        },
        "ads-per-party-per-date": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "spending-per-party-per-date": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "impressions-per-party-per-date": [[0] * NUMBER_OF_DATES for _ in PARTIES],
        "potential-reach-per-party-per-date": [[0] * NUMBER_OF_DATES for _ in PARTIES],
    }

    LOGGER.info(f"Creating party specific data.")

    party_specific_data = {
        party: {
            "last-updated": general_data["last-updated"],
            "start-date": general_data["start-date"],
            "total-ads": len(ads_per_party[party]),
            "spending-total-lower": sum(ad.spending_lower for ad in ads_per_party[party]),
            "spending-total-upper": sum(ad.spending_upper for ad in ads_per_party[party]),
            "spending-per-gender": [
                sum(a.spending_average * getattr(a, Ad.demographic_to_field_name(d)) for a in ads_per_party[party])
                for d in GENDERS
            ],
            "spending-per-age": [
                sum(a.spending_average * getattr(a, Ad.demographic_to_field_name(d)) for a in ads_per_party[party])
                for d in AGE_RANGES
            ],
            "spending-per-region": [
                sum(a.spending_average * getattr(a, Ad.demographic_to_field_name(d)) for a in ads_per_party[party])
                for d in REGIONS
            ],
            "impressions-per-gender": [
                sum(a.impressions_average * getattr(a, Ad.demographic_to_field_name(d)) for a in ads_per_party[party])
                for d in GENDERS
            ],
            "impressions-per-age": [
                sum(a.impressions_average * getattr(a, Ad.demographic_to_field_name(d)) for a in ads_per_party[party])
                for d in AGE_RANGES
            ],
            "impressions-per-region": [
                sum(a.impressions_average * getattr(a, Ad.demographic_to_field_name(d)) for a in ads_per_party[party])
                for d in REGIONS
            ],
            "spending-per-gender-per-date": [[0] * NUMBER_OF_DATES for _ in GENDERS],
            "spending-per-age-per-date": [[0] * NUMBER_OF_DATES for _ in AGE_RANGES],
            "spending-per-region-per-date": [[0] * NUMBER_OF_DATES for _ in REGIONS],
            "impressions-per-gender-per-date": [[0] * NUMBER_OF_DATES for _ in GENDERS],
            "impressions-per-age-per-date": [[0] * NUMBER_OF_DATES for _ in AGE_RANGES],
            "impressions-per-region-per-date": [[0] * NUMBER_OF_DATES for _ in REGIONS],
        }
        for party in PARTIES
    }

    for party_i, party in enumerate(PARTIES):
        LOGGER.info(f"Processing {len(ads_per_party[party])} ads for {party}.")
        for ad in ads_per_party[party]:
            for date_i in ad.active_date_indices():
                general_data["ads-per-party-per-date"][party_i][date_i] += 1
                general_data["spending-per-party-per-date"][party_i][date_i] += ad.average_spending_per_day
                general_data["impressions-per-party-per-date"][party_i][date_i] += ad.average_impressions_per_day
                general_data["potential-reach-per-party-per-date"][party_i][date_i] += ad.average_potential_reach_per_day

                for dem_type, demographic_list in (
                    ("gender", GENDERS),
                    ("age", AGE_RANGES),
                    ("region", REGIONS),
                ):
                    for dem_i, demographic in enumerate(demographic_list):
                        percentage = getattr(ad, Ad.demographic_to_field_name(demographic))

                        party_specific_data[party][f"spending-per-{dem_type}-per-date"][dem_i][date_i] += (
                            ad.average_spending_per_day * percentage
                        )
                        party_specific_data[party][f"impressions-per-{dem_type}-per-date"][dem_i][date_i] += (
                            ad.average_impressions_per_day * percentage
                        )

    recursive_round(general_data)
    recursive_round(party_specific_data)

    with open("../data/parsed_data/general-data.json", "w") as h_general_data:
        json.dump(general_data, h_general_data)

    for party in PARTIES:
        with open(f"../data/parsed_data/{party}.json", "w") as h_party_data:
            json.dump(party_specific_data[party], h_party_data)
