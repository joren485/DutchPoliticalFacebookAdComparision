import json

from datetime import datetime

from types import SimpleNamespace

from ad import Ad
from constants import DATETIME_FORMAT, PARTIES, GENDERS, AGES, REGIONS, DATES


def shorten_float(f):
    """Takes a float and removes trailing zeros."""
    f = float(f)
    if f.is_integer():
        return int(f)
    return round(f, 2)


statistics = SimpleNamespace(
    ads_total=0,
    ads_without_potential_reach=0,
    ads_per_party={p: 0 for p in PARTIES},
    ads_per_party_per_date={p: [0] * len(DATES) for p in PARTIES},
    # Spending statistics
    spending_total=0,
    spending_total_lower=0,
    spending_total_upper=0,
    spending_per_party={p: 0 for p in PARTIES},
    spending_per_party_per_date={p: [0] * len(DATES) for p in PARTIES},
    spending_per_party_per_region={p: {r: 0 for r in REGIONS} for p in PARTIES},
    spending_per_party_per_region_per_date={p: {r: [0] * len(DATES) for r in REGIONS} for p in PARTIES},
    spending_per_party_per_gender={p: {r: 0 for r in GENDERS} for p in PARTIES},
    spending_per_party_per_gender_per_date={p: {r: [0] * len(DATES) for r in GENDERS} for p in PARTIES},
    spending_per_party_per_age={p: {r: 0 for r in AGES} for p in PARTIES},
    spending_per_party_per_age_per_date={p: {r: [0] * len(DATES) for r in AGES} for p in PARTIES},
    most_expensive_ad=None,
    # Impressions statistics
    impressions_per_party={p: 0 for p in PARTIES},
    impressions_per_party_per_date={p: [0] * len(DATES) for p in PARTIES},
    impressions_per_party_per_region={p: {r: 0 for r in REGIONS} for p in PARTIES},
    impressions_per_party_per_region_per_date={p: {r: [0] * len(DATES) for r in REGIONS} for p in PARTIES},
    impressions_per_party_per_gender={p: {r: 0 for r in GENDERS} for p in PARTIES},
    impressions_per_party_per_gender_per_date={p: {r: [0] * len(DATES) for r in GENDERS} for p in PARTIES},
    impressions_per_party_per_age={p: {r: 0 for r in AGES} for p in PARTIES},
    impressions_per_party_per_age_per_date={p: {r: [0] * len(DATES) for r in AGES} for p in PARTIES},
    # Potential reach statistics
    potential_reach_per_party_per_date={p: [0] * len(DATES) for p in PARTIES},
)
if __name__ == "__main__":

    for party in PARTIES:
        party_data_path = f"../data/local_ad_archive/{party}.json"

        with open(party_data_path) as h_party:
            ads_data = [json.loads(ad_data) for ad_data in h_party.readlines()]

        Ad.parse_ads(ads_data, party, statistics)

    json_output = {
        "last_updated": datetime.now().strftime("%H:%M %d-%m-%Y"),
        "start-date": DATES[0].strftime(DATETIME_FORMAT),
        "days-total": len(DATES),
        "ads-total": statistics.ads_total,
        "spending-range": {
            "lower": round(statistics.spending_total_lower, 2),
            "upper": round(statistics.spending_total_upper, 2),
        },
        "most-expensive-ad": {
            "cost": statistics.most_expensive_ad.spending_average_per_day,
            "party": statistics.most_expensive_ad.party,
            "id": statistics.most_expensive_ad.id,
            "days": statistics.most_expensive_ad.active_days,
        },
        "ads-without-potential-reach": statistics.ads_without_potential_reach,
        "ads-per-party": {
            "map": statistics.ads_per_party,
            "order": list(
                k
                for k in sorted(
                    statistics.ads_per_party.keys(), reverse=True, key=lambda e: statistics.ads_per_party[e]
                )
            ),
        },
        "spending-per-party": {
            "map": statistics.spending_per_party,
            "order": list(
                k
                for k in sorted(
                    statistics.spending_per_party.keys(), reverse=True, key=lambda e: statistics.spending_per_party[e]
                )
            ),
        },
        "impressions-per-party": {
            "map": statistics.impressions_per_party,
            "order": list(
                k
                for k in sorted(
                    statistics.impressions_per_party.keys(),
                    reverse=True,
                    key=lambda e: statistics.impressions_per_party[e],
                )
            ),
        },
        "party-specific-data": {
            p: {
                "active-ads-per-date": statistics.ads_per_party_per_date[p],
                "spending-per-date": statistics.spending_per_party_per_date[p],
                "impressions-per-date": statistics.impressions_per_party_per_date[p],
                "potential-reach-per-date": statistics.potential_reach_per_party_per_date[p],
                "impressions-per-region": {
                    "map": statistics.impressions_per_party_per_region[p],
                    "order": list(
                        k
                        for k in sorted(
                            statistics.impressions_per_party_per_region[p].keys(),
                            reverse=True,
                            key=lambda e: statistics.impressions_per_party_per_region[p][e],
                        )
                    ),
                },
                "impressions-per-gender": {
                    "map": statistics.impressions_per_party_per_gender[p],
                    "order": list(
                        k
                        for k in sorted(
                            statistics.impressions_per_party_per_gender[p].keys(),
                            reverse=True,
                            key=lambda e: statistics.impressions_per_party_per_gender[p][e],
                        )
                    ),
                },
                "impressions-per-age": {
                    "map": statistics.impressions_per_party_per_age[p],
                    "order": list(
                        k
                        for k in sorted(
                            statistics.impressions_per_party_per_age[p].keys(),
                            reverse=True,
                            key=lambda e: statistics.impressions_per_party_per_age[p][e],
                        )
                    ),
                },
                "impressions-per-gender-per-date": {
                    g: statistics.impressions_per_party_per_gender_per_date[p][g] for g in GENDERS
                },
                "impressions-per-age-per-date": {
                    a: statistics.impressions_per_party_per_age_per_date[p][a] for a in AGES
                },
                "impressions-per-region-per-date": {
                    r: statistics.impressions_per_party_per_region_per_date[p][r] for r in REGIONS
                },
                "spending-per-region": {
                    "map": statistics.spending_per_party_per_region[p],
                    "order": list(
                        k
                        for k in sorted(
                            statistics.spending_per_party_per_region[p].keys(),
                            reverse=True,
                            key=lambda e: statistics.spending_per_party_per_region[p][e],
                        )
                    ),
                },
                "spending-per-gender": {
                    "map": statistics.spending_per_party_per_gender[p],
                    "order": list(
                        k
                        for k in sorted(
                            statistics.spending_per_party_per_gender[p].keys(),
                            reverse=True,
                            key=lambda e: statistics.spending_per_party_per_gender[p][e],
                        )
                    ),
                },
                "spending-per-age": {
                    "map": statistics.spending_per_party_per_age[p],
                    "order": list(
                        k
                        for k in sorted(
                            statistics.spending_per_party_per_age[p].keys(),
                            reverse=True,
                            key=lambda e: statistics.spending_per_party_per_age[p][e],
                        )
                    ),
                },
                "spending-per-gender-per-date": {
                    g: statistics.spending_per_party_per_gender_per_date[p][g] for g in GENDERS
                },
                "spending-per-age-per-date": {a: statistics.spending_per_party_per_age_per_date[p][a] for a in AGES},
                "spending-per-region-per-date": {
                    r: statistics.spending_per_party_per_region_per_date[p][r] for r in REGIONS
                },
            }
            for p in PARTIES
        },
    }

    json_output = json.loads(json.dumps(json_output), parse_float=shorten_float)

    with open("../data/data.json", "w") as h_file:
        json.dump(json_output, h_file, sort_keys=True)
