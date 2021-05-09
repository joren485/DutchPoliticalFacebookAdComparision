import json
import logging
from datetime import datetime
from typing import Union

from constants import AGE_RANGES, DATETIME_FORMAT, FIRST_DATE, GENDERS, NUMBER_OF_DATES, PARTIES, REGIONS

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
    elif isinstance(o, list) and isinstance(o[0], (list, dict)):
        for object_element in o:
            recursive_round(object_element, precision)
    elif isinstance(o, list) and isinstance(o[0], (int, float)):
        for object_index, object_element in enumerate(o):
            o[object_index] = round(object_element, precision)


ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))
ads_per_party = {p: [ad for ad in ads if ad.party == p] for p in PARTIES}

most_expensive_ad = max(ads, key=lambda e: e.average_spending_per_day)

general_output_data = {
    "last-updated": datetime.now().strftime("%H:%M %d-%m-%Y"),
    "start-date": FIRST_DATE.strftime(DATETIME_FORMAT),
    "ads-total": len(ads),
    "ads-without-potential-reach": sum(1 for a in ads if not a.has_potential_reach),
    "ads-per-party": [len(ads_per_party[p]) for p in PARTIES],
    "spending-total-range": (
        sum(ad.spending_lower for ad in ads),
        sum(ad.spending_upper for ad in ads),
    ),
    "spending-per-party": [
        sum(ad.spending_average for ad in ads_per_party[p]) for p in PARTIES
    ],
    "impressions-per-party": [
        sum(ad.impressions_average for ad in ads_per_party[p]) for p in PARTIES
    ],
    "most-expensive-ad": {
        "id": most_expensive_ad.ad_id,
        "party": most_expensive_ad.party,
        "spend-per-day": most_expensive_ad.average_spending_per_day,
        "days": most_expensive_ad.days_active,
    },
    "active-ads-per-party-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for p in PARTIES],
    "spending-per-party-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for p in PARTIES],
    "impressions-per-party-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for p in PARTIES],
    "potential-reach-per-party-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for p in PARTIES],
}

party_specific_output_data = {
    party: {
        "last-updated": general_output_data["last-updated"],
        "start-date": general_output_data["start-date"],
        "total-ads": len(ads_per_party[party]),
        "spending-total-range": (
            sum(ad.spending_lower for ad in ads_per_party[party]),
            sum(ad.spending_upper for ad in ads_per_party[party]),
        ),
        "spending-per-gender": [0 for _ in GENDERS],
        "spending-per-gender-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for _ in GENDERS],
        "spending-per-age": [0 for _ in AGE_RANGES],
        "spending-per-age-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for _ in AGE_RANGES],
        "spending-per-region": [0 for _ in REGIONS],
        "spending-per-region-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for _ in REGIONS],
        "impressions-per-gender": [0 for _ in GENDERS],
        "impressions-per-gender-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for _ in GENDERS],
        "impressions-per-age": [0 for _ in AGE_RANGES],
        "impressions-per-age-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for _ in AGE_RANGES],
        "impressions-per-region": [0 for _ in REGIONS],
        "impressions-per-region-per-date": [[0 for _ in range(NUMBER_OF_DATES)] for _ in REGIONS],
    }
    for party in PARTIES
}

for party_index, party in enumerate(PARTIES):
    LOGGER.info(f"Processing {len(ads_per_party[party])} ads for {party}.")
    for ad in ads_per_party[party]:

        for distribution, distribution_list in (("gender", GENDERS),
                                                ("age", AGE_RANGES),
                                                ("region", REGIONS),):
            for distribution_type_index, distribution_type in enumerate(distribution_list):
                field_name = Ad.distribution_type_to_field_name(distribution_type)
                percentage = getattr(ad, field_name)

                party_specific_output_data[party][f"spending-per-{distribution}"][distribution_type_index] += ad.spending_average * percentage
                party_specific_output_data[party][f"impressions-per-{distribution}"][distribution_type_index] += ad.impressions_average * percentage

        for date_index in ad.active_date_indices():
            general_output_data["active-ads-per-party-per-date"][party_index][date_index] += 1
            general_output_data["spending-per-party-per-date"][party_index][date_index] += ad.average_spending_per_day
            general_output_data["impressions-per-party-per-date"][party_index][date_index] += ad.average_impressions_per_day
            general_output_data["potential-reach-per-party-per-date"][party_index][date_index] += ad.average_potential_reach_per_day

            for distribution, distribution_list in (("gender", GENDERS),
                                                    ("age", AGE_RANGES),
                                                    ("region", REGIONS),):
                for distribution_type_index, distribution_type in enumerate(distribution_list):
                    field_name = Ad.distribution_type_to_field_name(distribution_type)
                    percentage = getattr(ad, field_name)

                    party_specific_output_data[party][f"spending-per-{distribution}-per-date"][distribution_type_index][date_index] += ad.average_spending_per_day * percentage
                    party_specific_output_data[party][f"impressions-per-{distribution}-per-date"][distribution_type_index][date_index] += ad.average_impressions_per_day * percentage

recursive_round(general_output_data)
recursive_round(party_specific_output_data)

with open("../data/parsed_data/general-data.json", "w") as h_general_data:
    json.dump(general_output_data, h_general_data)

for party in PARTIES:
    with open(f"../data/parsed_data/{party}.json", "w") as h_party_data:
        json.dump(party_specific_output_data[party], h_party_data)
