import json
import logging

from datetime import datetime

from models import Ad

from constants import FIRST_DATE, PARTIES, DATETIME_FORMAT, NUMBER_OF_DATES, GENDERS, AGE_RANGES, REGIONS

from collections import Counter

from processing import recursive_round

NUMBER_OF_COMMON_WORDS = 10

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

RANKS = [f"{data_type}-{demographic.lower()}"
         for demographic in ["total"] + GENDERS + AGE_RANGES + REGIONS
         for data_type in ("occurrences", "impressions")]

party_data = {
    p: {
        "last-updated": datetime.now().strftime("%H:%M %d-%m-%Y"),
    }
    for p in PARTIES
}

for p in PARTIES:
    for r in RANKS:
        party_data[p][r] = {
            "labels": [],
            "data": [],
        }

ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))
ads_per_party = {p: [ad for ad in ads if ad.party == p] for p in PARTIES}

for party in PARTIES:

    for rank in RANKS:
        LOGGER.info(f"{party}: {rank}")

        party_text_counter = Counter()
        for ad in ads_per_party[party]:
            for word in ad.parsed_text:
                party_text_counter.update({word: ad.rank_to_data(rank)})

        for word, occurrences in party_text_counter.most_common(NUMBER_OF_COMMON_WORDS):
            party_data[party][rank]["labels"].append(word)
            party_data[party][rank]["data"].append(occurrences)

recursive_round(party_data)

for party in PARTIES:
    with open(f"../data/parsed_data/text-{party}.json", "w") as h_party_data:
        json.dump(party_data[party], h_party_data)
