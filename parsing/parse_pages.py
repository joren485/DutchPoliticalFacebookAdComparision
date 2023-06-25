import csv
import json

import requests

from constants import PARTIES

from datetime import date, timedelta

SEARCH_MAP = {
    "50+": "50P",
    "CU": "ChristenUnie",
    "GL": "Groenlinks",
    "PvdD": "Partij voor de Dieren",
}


def get_spending_report(party, cursor=None):
    """Retrieve Facebook page ids linked to parties from the Facebook Ad library spending report."""
    page_ids = {}

    url = (
        "https://www.facebook.com/ads/library/report/async/advertiser_data/"
        f"?report_ds={(date.today() - timedelta(days=2)).strftime('%Y-%m-%d')}&"
        "country=NL"
        "&time_preset=lifelong"
        "&sort_column=spend"
        "&component_id=advertiser_table"
        f"&q={party}"
    )

    if cursor is not None:
        url += f"&encrypted_forward_cursor={cursor}"

    print(url)
    r = requests.post(url, data={"__a": 1})

    payload = json.loads(r.text[len("for (;;);") :])["payload"]

    for advertiser in payload["advertisers"]:
        page_ids[str(advertiser["advertiserPageID"])] = advertiser["advertiserPage"]

    if payload["advertiserCursors"]["encryptedForwardCursor"] is not None:
        page_ids.update(get_spending_report(party, payload["advertiserCursors"]["encryptedForwardCursor"]))

    return page_ids


party_pages = {}
for p in PARTIES:
    print(p)

    if p in SEARCH_MAP:
        party_pages[p] = get_spending_report(SEARCH_MAP[p])
    else:
        party_pages[p] = get_spending_report(p)


with open("../data/facebook_page_ids.csv", "w", newline="") as h_file:
    writer = csv.DictWriter(h_file, ["Party", "Page Name", "Page ID"], quoting=csv.QUOTE_ALL)

    writer.writeheader()
    for party in sorted(party_pages.keys()):
        for page_id, page_name in sorted(party_pages[party].items(), key=lambda e: e[1]):
            writer.writerow(
                {
                    "Party": party,
                    "Page Name": page_name,
                    "Page ID": page_id,
                }
            )
