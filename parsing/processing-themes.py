
from constants import FIRST_DATE, PARTIES, DEMOGRAPHIC_TYPES, DEMOGRAPHIC_TYPE_TO_LIST_MAP

from themes import Theme

from models import Ad

from utils import render_template, recursive_round

THEMES = [t for t in Theme if t != Theme.NONE]
THEME_NAMES = [t.name for t in Theme if t != Theme.NONE]

if __name__ == "__main__":

    theme_data = {

        "impressions-demographics-theme": {
            t: {
                dt: [] for dt in DEMOGRAPHIC_TYPES
            } for t in THEME_NAMES
        },

        "impressions-demographics-theme-party": {
            p: {
                t: {
                    dt: [] for dt in DEMOGRAPHIC_TYPES
                } for t in THEME_NAMES
            } for p in PARTIES
        },

        "number-of-ads-theme-party": {
            p: [] for p in PARTIES
        },
    }

    for theme in THEMES:

        ads = Ad.select().where(Ad.start_date >= FIRST_DATE).where(Ad.themes.bin_and(theme.value) == theme.value)
        for demographic_type in DEMOGRAPHIC_TYPES:
            for demographic in DEMOGRAPHIC_TYPE_TO_LIST_MAP[demographic_type]:
                theme_data["impressions-demographics-theme"][theme.name][demographic_type].append(
                    sum(a.rank_to_data("impressions", demographic) for a in ads)
                )

        for party in PARTIES:
            ads = Ad.select().where(Ad.start_date >= FIRST_DATE).where(Ad.party == party).where(Ad.themes.bin_and(theme.value) == theme.value)

            theme_data["number-of-ads-theme-party"][party].append(ads.count())

            for demographic_type in DEMOGRAPHIC_TYPES:
                for demographic in DEMOGRAPHIC_TYPE_TO_LIST_MAP[demographic_type]:
                    theme_data["impressions-demographics-theme-party"][party][theme.name][demographic_type].append(
                        sum(a.rank_to_data("impressions", demographic) for a in ads)
                    )

    recursive_round(theme_data)
    render_template("themes.html", "themes.html", theme_data=theme_data, THEMES=THEME_NAMES)
