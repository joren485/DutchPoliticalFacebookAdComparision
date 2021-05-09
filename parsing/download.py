import argparse
import csv
import json
import logging
from datetime import date, timedelta
from typing import List

import requests

from constants import (
    DATETIME_FORMAT,
    FACEBOOK_API_URL,
    MAX_PAGE_IDS_PER_REQUEST,
    PARTIES,
)

from models import Ad

from parsing import json_to_ad_dict

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def download_ads(api_url: str, current_party: str) -> None:
    """
    Request ads from the Facebook Ad Library API.

    Parse and write all found ads.
    If the request returns a paging url, a recursive call is made to follow that url.

    :param api_url: The url to request.
    :param current_party: The party we are requesting ads for.
    """
    response = requests.get(api_url)
    response_data = response.json()

    if "error" in response_data:
        LOGGER.error(f"Error from API: '{response_data['error']}'")
        return

    if len(response_data["data"]) > 0:
        LOGGER.info(f"Got {len(response_data['data'])} ads ({current_party})")
        Ad.insert_many(
            json_to_ad_dict(ad, current_party) for ad in response_data["data"]
        ).on_conflict_replace().execute()

    if "paging" in response_data:
        LOGGER.info("Got paged ads")
        download_ads(response_data["paging"]["next"], current_party)


def parse_facebook_page_ids(parties: List[str]) -> dict[str, List[str]]:
    """
    Create a map from parties to Facebook page ids from facebook_page_ids.csv.

    :param parties: The parties to put in the map
    :return: A dict that maps a party to a list of their Facebook page ids.
    """
    page_ids_dict = {p: [] for p in parties}
    with open("../data/facebook_page_ids.csv") as h_page_ids:
        reader = csv.DictReader(h_page_ids)
        for row in reader:

            if row["Party"] not in parties:
                if row["Party"] not in PARTIES:
                    LOGGER.warning(f"Unknown party: '{row['Party']}'")
                continue

            page_ids_dict[row["Party"]].append(row["Page ID"])

    return page_ids_dict


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-a", "--all", action="store_true")
    parser.add_argument("-p", "--parties")

    args = parser.parse_args()
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    if args.parties:
        page_ids_per_party = parse_facebook_page_ids(
            [p for p in args.parties.split(",") if p in PARTIES]
        )
    else:
        page_ids_per_party = parse_facebook_page_ids(PARTIES)

    for party, page_ids in page_ids_per_party.items():

        for i in range(0, len(page_ids), MAX_PAGE_IDS_PER_REQUEST):
            page_ids_subset = page_ids[i : i + MAX_PAGE_IDS_PER_REQUEST]

            LOGGER.info(
                f"Downloading ads of {len(page_ids_subset)} pages ({i}/{len(page_ids)}) ({party})"
            )

            download_ads(
                FACEBOOK_API_URL.format(
                    page_ids=",".join(page_ids_subset),
                    min_date=(date.today() - timedelta(weeks=1)).strftime(
                        DATETIME_FORMAT
                    )
                    if not args.all
                    else "2018-05-07",  # This is the first allowed day.
                ),
                party,
            )
