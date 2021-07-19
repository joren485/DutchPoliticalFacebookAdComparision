import json
import logging

from constants import DATA_TYPES, DEMOGRAPHICS, DEMOGRAPHIC_TYPES, DEMOGRAPHIC_TYPE_TO_LIST_MAP, FIRST_DATE, PARTIES, THEMES

from models import Ad

from processing import recursive_round

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

RANKS = [(data_type, demographic)
         for demographic in DEMOGRAPHICS
         for data_type in DATA_TYPES]

ads = list(Ad.select().where(Ad.start_date >= FIRST_DATE))

theme_data = {
    t: {
        "general": {
            f"{data_type}-{demographic}": [0 for _ in PARTIES]
            for data_type, demographic in RANKS
        },
    } for t in THEMES
}

for theme in THEMES:
    logging.info(f"Theme: {theme}")

    for party in PARTIES:
        theme_data[theme][party] = {}

        for data_type in DATA_TYPES:
            for demographic_type in DEMOGRAPHIC_TYPES:
                demographic_list = DEMOGRAPHIC_TYPE_TO_LIST_MAP[demographic_type]
                theme_data[theme][party][f"{data_type}-{demographic_type}"] = [0 for _ in demographic_list]

    for ad in ads:
        if ad.is_about_theme(theme):
            for data_type, demographic in RANKS:
                theme_data[theme]["general"][f"{data_type}-{demographic}"][PARTIES.index(ad.party)] += ad.rank_to_data(data_type, demographic)

            for data_type in DATA_TYPES:
                for demographic_type in DEMOGRAPHIC_TYPES:
                    demographic_list = DEMOGRAPHIC_TYPE_TO_LIST_MAP[demographic_type]

                    for index, demographic in enumerate(demographic_list):
                        theme_data[theme][ad.party][f"{data_type}-{demographic_type}"][index] += ad.rank_to_data(
                            data_type, demographic
                        )

recursive_round(theme_data)

with open("../data/parsed_data/text-theme.json", "w") as h_json:
    json.dump(theme_data, h_json)
