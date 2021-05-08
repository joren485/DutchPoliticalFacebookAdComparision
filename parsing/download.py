import csv
import argparse
import logging
import json

import requests

from datetime import date, timedelta

from constants import (
    PARTIES,
    MAX_PAGE_IDS_PER_REQUEST,
    FACEBOOK_API_URL,
    DATETIME_FORMAT,
)

from models import Ad

from parsing import json_to_ad_dict

LOGGER = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def download_ads(api_url, party):
    response = requests.get(api_url)
    response_data = response.json()

    if "error" in response_data:
        LOGGER.error(f"Error from API: '{response_data['error']}'")
        return

    if len(response_data["data"]) > 0:
        LOGGER.info(f"Got {len(response_data['data'])} ads ({party})")
        Ad.insert_many(
            json_to_ad_dict(ad, party) for ad in response_data["data"]
        ).on_conflict_replace().execute()

    if "paging" in response_data:
        download_ads(response_data["paging"]["next"], party)


def parse_facebook_page_ids(parties):
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


def parse_existing_ad_ids(path):
    try:
        with open(path) as h_ids_file:
            return [json.loads(line)["id"] for line in h_ids_file.readlines()]
    except FileNotFoundError:
        return []


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
