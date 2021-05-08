import json

from datetime import datetime

from models import Ad
from constants import FIRST_DATE, PARTIES, DATETIME_FORMAT, REGIONS, GENDERS, AGE_RANGES, NUMBER_OF_DATES


def round_list(l, precision=2):
    for i, e in enumerate(l):
        l[i] = round(e, precision)


ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))
ads_per_party = {p: [ad for ad in ads if ad.party == p] for p in PARTIES}

most_expensive_ad = max(ads, key=lambda e: e.average_spending_per_day)

general_output_data = {
    "last-updated": datetime.now().strftime("%H:%M %d-%m-%Y"),
    "start-date": FIRST_DATE.strftime(DATETIME_FORMAT),
    "ads-total": len(ads),
    "ads-without-potential-reach": len(
        [a for a in ads if a.potential_reach_upper is None]
    ),
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
        "cost": most_expensive_ad.average_spending_per_day,
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
    for ad in ads_per_party[party]:

        for gender_index, gender in enumerate(GENDERS):
            field_name = Ad.distribution_type_to_field_name(gender)
            percentage = getattr(ad, field_name)

            party_specific_output_data[party]["spending-per-gender"][gender_index] += ad.spending_average * percentage
            party_specific_output_data[party]["impressions-per-gender"][gender_index] += ad.impressions_average * percentage

        for age_range_index, age_range in enumerate(AGE_RANGES):
            field_name = Ad.distribution_type_to_field_name(age_range)
            percentage = getattr(ad, field_name)

            party_specific_output_data[party]["spending-per-age"][age_range_index] += ad.spending_average * percentage
            party_specific_output_data[party]["impressions-per-age"][age_range_index] += ad.impressions_average * percentage

        for region_index, region in enumerate(REGIONS):
            field_name = Ad.distribution_type_to_field_name(region)
            percentage = getattr(ad, field_name)

            party_specific_output_data[party]["spending-per-region"][region_index] += ad.spending_average * percentage
            party_specific_output_data[party]["impressions-per-region"][region_index] += ad.impressions_average * percentage

        for date_index, date in ad.dates_active():
            general_output_data["active-ads-per-party-per-date"][party_index][date_index] += 1
            general_output_data["spending-per-party-per-date"][party_index][date_index] += ad.average_spending_per_day
            general_output_data["impressions-per-party-per-date"][party_index][date_index] += ad.average_impressions_per_day
            general_output_data["potential-reach-per-party-per-date"][party_index][date_index] += ad.average_potential_reach_per_day

            for gender_index, gender in enumerate(GENDERS):
                field_name = Ad.distribution_type_to_field_name(gender)
                percentage = getattr(ad, field_name)

                party_specific_output_data[party]["spending-per-gender-per-date"][gender_index][date_index] += ad.average_spending_per_day * percentage
                party_specific_output_data[party]["impressions-per-gender-per-date"][gender_index][date_index] += ad.average_impressions_per_day * percentage

            for age_range_index, age_range in enumerate(AGE_RANGES):
                field_name = Ad.distribution_type_to_field_name(age_range)
                percentage = getattr(ad, field_name)

                party_specific_output_data[party]["spending-per-age-per-date"][age_range_index][date_index] += ad.average_spending_per_day * percentage
                party_specific_output_data[party]["impressions-per-age-per-date"][age_range_index][date_index] += ad.average_impressions_per_day * percentage

            for region_index, region in enumerate(REGIONS):
                field_name = Ad.distribution_type_to_field_name(region)
                percentage = getattr(ad, field_name)

                party_specific_output_data[party]["spending-per-region-per-date"][region_index][date_index] += ad.average_spending_per_day * percentage
                party_specific_output_data[party]["impressions-per-region-per-date"][region_index][date_index] += ad.average_impressions_per_day * percentage

    round_list(general_output_data["spending-per-party-per-date"][party_index])
    round_list(general_output_data["impressions-per-party-per-date"][party_index])
    round_list(general_output_data["spending-per-party-per-date"][party_index])

    round_list(party_specific_output_data[party]["spending-per-gender"])
    round_list(party_specific_output_data[party]["spending-per-age"])
    round_list(party_specific_output_data[party]["spending-per-region"])
    round_list(party_specific_output_data[party]["impressions-per-gender"])
    round_list(party_specific_output_data[party]["impressions-per-age"])
    round_list(party_specific_output_data[party]["impressions-per-region"])

    for i in range(len(GENDERS)):
        round_list(party_specific_output_data[party]["spending-per-gender-per-date"][i])
        round_list(party_specific_output_data[party]["impressions-per-gender-per-date"][i])

    for i in range(len(AGE_RANGES)):
        round_list(party_specific_output_data[party]["spending-per-age-per-date"][i])
        round_list(party_specific_output_data[party]["impressions-per-age-per-date"][i])

    for i in range(len(REGIONS)):
        round_list(party_specific_output_data[party]["spending-per-region-per-date"][i])
        round_list(party_specific_output_data[party]["impressions-per-region-per-date"][i])


with open("../data/parsed_data/general-data.json", "w") as h_general_data:
    json.dump(general_output_data, h_general_data)

for party in PARTIES:
    with open(f"../data/parsed_data/{party}.json", "w") as h_party_data:
        json.dump(party_specific_output_data[party], h_party_data)
