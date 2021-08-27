import os
from datetime import date

LOCAL_AD_ARCHIVE_PATH = "../data/local_ad_archive.sqlite"

AD_LIMIT_PER_REQUEST = 1000
MAX_PAGE_IDS_PER_REQUEST = 10

FACEBOOK_API_VERSION = "v11.0"

FACEBOOK_API_FIELDS = [
    "id",
    "ad_creation_time",
    "ad_creative_bodies",
    "ad_creative_link_captions",
    "ad_creative_link_descriptions",
    "ad_creative_link_titles",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "currency",
    "delivery_by_region",
    "demographic_distribution",
    "impressions",
    "languages",
    "page_id",
    "potential_reach",
    "spend",
]

FACEBOOK_API_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_API_URL = (
    f"https://graph.facebook.com/{FACEBOOK_API_VERSION}/ads_archive?"
    f"access_token={FACEBOOK_API_ACCESS_TOKEN}&"
    f"limit={AD_LIMIT_PER_REQUEST}&"
    f"fields={','.join(FACEBOOK_API_FIELDS)}&"
    f"ad_reached_countries=NL&"
    f"ad_active_status=all&"
    f"ad_delivery_date_min={{min_date}}&"
    f"search_page_ids={{page_ids}}"
)

DATETIME_FORMAT = "%Y-%m-%d"
FIRST_DATE = date(
    year=date.today().year - 1, month=date.today().month, day=date.today().day
)
NUMBER_OF_DATES = (date.today() - FIRST_DATE).days + 1

CURRENCY_EXCHANGE_RATE_MAP = {
    "EUR": 1,
    "USD": 0.85,
}

THEMES = {
    "klimaat": [
        "klimaat",
        "duurzaam",
        "groen",
        "green",
        "kernenergie",
        "co2",
        "windmolen",
        "windturbines",
        "zonnepaneel",
        "zonnepanelen",
        "vervuiling",
        "vervuilend",
        "stroom",
        "energie",
        "biomassa",
        "stikstof",
    ],
    "onderwijs": [
        "onderwijs",
        "opleiding",
        "kennis",
        "universiteit",
        "docent",
        "leraar",
        "leraren",
        "school",
        "scholen",
        "wetenschap",
        "onderzoek",
        "studiefinanciering",
        "leenstelsel",
        "studievoorschot",
        "mbo",
        "klassen",
    ],
    "gezondheidszorg": [
        "gezondheid",
        "zorg",
        "ziek",
        "arts",
        "dokter",
        "corona",
        "covid",
        "ic-capaciteit",
        "verzekering",
        "verzekeraar",
        "farmaceutisch",
        "bejaard",
        "verpleeg",
        "eigen risico",
        "virus",
    ],
}

PARTIES = [
    "50+",
    "BIJ1",
    "BBB",
    "CDA",
    "CU",
    "D66",
    "DENK",
    "FvD",
    "GL",
    "JA21",
    "PVV",
    "PvdA",
    "PvdD",
    "SGP",
    "SP",
    "VOLT",
    "VVD",
]

GENDERS = ["female", "male"]

AGE_RANGES = [
    "13-17",
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65+",
]

REGIONS = [
    "Drenthe",
    "Flevoland",
    "Friesland",
    "Gelderland",
    "Groningen",
    "Limburg",
    "Noord-Brabant",
    "Noord-Holland",
    "Overijssel",
    "Utrecht",
    "Zeeland",
    "Zuid-Holland",
]

GENDER_IGNORE_LIST = [
    "Unknown",
    "unknown",
]

REGION_IGNORE_LIST = [
    "Unknown",
    "Nordrhein-Westfalen",
    "Flemish Region",
    "Niedersachsen",
    "Wallonia",
    "Brussels",
    "Mandalay",
    "Bonaire, Sint Eustatius and Saba",
    "Aruba",
    "Curaçao",
]

DEMOGRAPHIC_TYPES = ["total", "gender", "age", "region"]
DEMOGRAPHICS = ["total"] + GENDERS + AGE_RANGES + REGIONS
DEMOGRAPHIC_TYPE_TO_LIST_MAP = {
    "total": ["total"],
    "gender": GENDERS,
    "age": AGE_RANGES,
    "region": REGIONS,
}

DATA_TYPES = ["number-of-ads", "spending", "impressions", "potential-reach"]
