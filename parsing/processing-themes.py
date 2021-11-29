import logging

from constants import (
    DEMOGRAPHIC_TYPE_TO_LIST_MAP,
    DEMOGRAPHIC_TYPES,
    FIRST_DATE,
    PARTIES,
)
from models import Ad
from themes import Theme
from utils import recursive_round, render_template

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":

    theme_data = {
        "impressions-demographics-theme": {
            t: {dt: [] for dt in DEMOGRAPHIC_TYPES} for t in Theme.titles()
        },
        "impressions-demographics-theme-party": {
            p: {t: {dt: [] for dt in DEMOGRAPHIC_TYPES} for t in Theme.titles()}
            for p in PARTIES
        },
        "impressions-theme-party": {p: [] for p in PARTIES},
        "number-of-ads-theme-party": {p: [] for p in PARTIES},
        "matched": {
            p: [
                Ad.select()
                .where(Ad.start_date >= FIRST_DATE)
                .where(Ad.themes != 0)
                .where(Ad.party == p)
                .count(),
                Ad.select()
                .where(Ad.start_date >= FIRST_DATE)
                .where(Ad.themes == 0)
                .where(Ad.party == p)
                .count(),
            ]
            for p in PARTIES
        },
    }

    for theme in Theme.all():
        logging.info(f"Processing {theme.title}.")

        ads = (
            Ad.select()
            .where(Ad.start_date >= FIRST_DATE)
            .where(Ad.themes.bin_and(theme.value) == theme.value)
        )
        for demographic_type in DEMOGRAPHIC_TYPES:
            for demographic in DEMOGRAPHIC_TYPE_TO_LIST_MAP[demographic_type]:
                theme_data["impressions-demographics-theme"][theme.title][
                    demographic_type
                ].append(sum(a.rank_to_data("impressions", demographic) for a in ads))

        for party in PARTIES:
            ads = (
                Ad.select()
                .where(Ad.start_date >= FIRST_DATE)
                .where(Ad.party == party)
                .where(Ad.themes.bin_and(theme.value) == theme.value)
            )

            theme_data["number-of-ads-theme-party"][party].append(ads.count())
            theme_data["impressions-theme-party"][party].append(
                sum(a.rank_to_data("impressions", "total") for a in ads)
            )

            for demographic_type in DEMOGRAPHIC_TYPES:
                for demographic in DEMOGRAPHIC_TYPE_TO_LIST_MAP[demographic_type]:
                    theme_data["impressions-demographics-theme-party"][party][
                        theme.title
                    ][demographic_type].append(
                        sum(a.rank_to_data("impressions", demographic) for a in ads)
                    )

    logging.debug("Writing templates.")
    recursive_round(theme_data)
    render_template(
        "themes.html", "themes.html", theme_data=theme_data, THEMES=Theme.titles()
    )
