import logging
from datetime import date

from constants import (
    DATA_TYPES,
    DEMOGRAPHIC_TYPE_TO_LIST_MAP,
    DEMOGRAPHIC_TYPES,
    PARTIES,
)
from models import Ad
from utils import recursive_round, render_template, time_range_len

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

JAN_1 = date(year=2021, month=1, day=1)
MAR_17 = date(year=2021, month=3, day=17)

NUMBER_OF_DATES = time_range_len(start_date=JAN_1, end_date=MAR_17)

if __name__ == "__main__":

    ads_per_party = {
        p: Ad.ads_in_time_range(first_date=JAN_1, last_date=MAR_17).where(Ad.party == p) for p in PARTIES
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
                    for date_i in ad.active_date_indices(first_date=JAN_1, last_date=MAR_17):
                        for demographic_i, demographic in enumerate(demographic_list):
                            party_data[f"{data_type}-{demographic_type}-daily"][
                                demographic_i
                            ][date_i] += ad.rank_to_data(
                                data_type, demographic, per_day=True
                            )

        logging.debug(f"Writing template for { party }.")
        recursive_round(party_data)
        render_template(
            "party.html",
            f"{party.lower()}.html",
            party=party,
            party_data=party_data,
        )
