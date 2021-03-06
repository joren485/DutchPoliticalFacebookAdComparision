import json
import logging
from collections import Counter
from datetime import datetime

from constants import AGE_RANGES, FIRST_DATE, GENDERS, LEADERS, PARTIES, REGIONS

from models import Ad

from processing import recursive_round

NUMBER_OF_COMMON_WORDS = 10

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

RANKS = [(data_type, demographic.lower())
         for demographic in ["total"] + GENDERS + AGE_RANGES + REGIONS
         for data_type in ("occurrences", "impressions", "potential-reach")]

ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))
ads_per_party = {p: [ad for ad in ads if ad.party == p] for p in PARTIES}

party_data = {
    p: {
        "last-updated": datetime.now().strftime("%H:%M %d-%m-%Y"),
    }
    for p in PARTIES
}

for p in PARTIES:
    for data_type in ("occurrences", "impressions", "potential-reach"):
        party_data[p][f"{data_type}-leaders"] = {
            "labels": [],
            "data": [],
        }

    for data_type, demographic in RANKS:
        party_data[p][f"{data_type}-{demographic}"] = {
            "labels": [],
            "data": [],
        }

for party in PARTIES:

    for data_type, demographic in RANKS:
        LOGGER.info(f"{party}: {data_type}-{demographic}")

        party_text_counter = Counter()
        for ad in ads_per_party[party]:
            for word in ad.parsed_text:
                party_text_counter.update({word: ad.rank_to_data(data_type, demographic)})

        if demographic == "total":
            for name in LEADERS:
                count = party_text_counter[name.rsplit(" ", 1)[-1].lower()]
                if count > 0:
                    party_data[party][f"{data_type}-leaders"]["labels"].append(name)
                    party_data[party][f"{data_type}-leaders"]["data"].append(count)

        for word, count in party_text_counter.most_common(NUMBER_OF_COMMON_WORDS):
            if count > 0:
                party_data[party][f"{data_type}-{demographic}"]["labels"].append(word)
                party_data[party][f"{data_type}-{demographic}"]["data"].append(count)

recursive_round(party_data)

for party in PARTIES:
    with open(f"../data/parsed_data/text-{party}.json", "w") as h_party_data:
        json.dump(party_data[party], h_party_data)
