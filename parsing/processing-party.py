import logging

from constants import (
    FIRST_DATE,
    NUMBER_OF_DATES,
    PARTIES,
    DEMOGRAPHIC_TYPE_TO_LIST_MAP,
    DATA_TYPES,
    DEMOGRAPHIC_TYPES,
)

from models import Ad

from utils import recursive_round, render_template

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


if __name__ == "__main__":

    ads_per_party = {
        p: Ad.select().where(Ad.start_date >= FIRST_DATE).where(Ad.party == p)
        for p in PARTIES
    }

    for party in PARTIES:
        logging.info(f"Processing {len(ads_per_party[party])} ads for {party}.")

        party_data = {
            "total-ads": len(ads_per_party[party]),
            "spending-total-lower": sum(
                ad.spending_lower for ad in ads_per_party[party]
            ),
            "spending-total-upper": sum(
                ad.spending_upper for ad in ads_per_party[party]
            ),
        }

        for data_type in DATA_TYPES:
            for demographic_type in DEMOGRAPHIC_TYPES:
                demographic_list = DEMOGRAPHIC_TYPE_TO_LIST_MAP[demographic_type]

                party_data[f"{data_type}-{demographic_type}"] = [
                    sum(
                        ad.rank_to_data(data_type, demographic)
                        for ad in ads_per_party[party]
                    )
                    for demographic in demographic_list
                ]

                party_data[f"{data_type}-{demographic_type}-daily"] = [
                    [0] * NUMBER_OF_DATES for _ in demographic_list
                ]

                for ad in ads_per_party[party]:
                    for date_i in ad.active_date_indices():
                        for demographic_i, demographic in enumerate(demographic_list):
                            party_data[f"{data_type}-{demographic_type}-daily"][
                                demographic_i
                            ][date_i] += ad.rank_to_data(
                                data_type, demographic, per_day=True
                            )

        logging.debug(f"Writing template for { party }")
        recursive_round(party_data)
        render_template(
            "party.html",
            f"{party.lower()}.html",
            party=party,
            party_data=party_data,
        )
