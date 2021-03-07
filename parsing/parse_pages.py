from bs4 import BeautifulSoup

import os

import csv

RAW_DATA_DIRECTORY = "../data/raw_ad_library_spending_report"

party_pages = {
    "50P": {},
    "BIJ1": {},
    "CDA": {},
    "CO": {},
    "CU": {},
    "D66": {},
    "DENK": {},
    "FvD": {},
    "GL": {},
    "JA21": {},
    "PVV": {},
    "PvdA": {},
    "PvdD": {},
    "SGP": {},
    "SP": {},
    "VVD": {},
    "VOLT": {},
}

for filename in os.listdir(RAW_DATA_DIRECTORY):

    if not filename.endswith("html"):
        continue

    party = filename[: filename.index(".")]

    path = os.path.join(RAW_DATA_DIRECTORY, filename)

    with open(path) as h_file:
        parser = BeautifulSoup(h_file.read(), "html5lib")

    for anchor in parser.find_all("a"):
        page_id = anchor["href"][59:]
        page_name = anchor.find("div", {"class": "_7vgw"}).text
        page_name = page_name.replace(" (This Page has been deleted.)", "")

        if party == "SP" and "SP" not in page_name and "sp" in page_name.lower():
            continue

        party_pages[party][page_id] = page_name


with open("../data/facebook_page_ids.csv", "w", newline="") as h_file:
    writer = csv.DictWriter(
        h_file, ["Party", "Page Name", "Page ID"], quoting=csv.QUOTE_ALL
    )

    writer.writeheader()
    for party in sorted(party_pages.keys()):
        for page_id, page_name in sorted(
            party_pages[party].items(), key=lambda e: e[1]
        ):
            writer.writerow(
                {
                    "Party": party,
                    "Page Name": page_name,
                    "Page ID": page_id,
                }
            )
