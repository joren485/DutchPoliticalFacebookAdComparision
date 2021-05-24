import os
from datetime import date

LOCAL_AD_ARCHIVE_PATH = "../data/local_ad_archive.sqlite"

AD_LIMIT_PER_REQUEST = 1000
MAX_PAGE_IDS_PER_REQUEST = 10

FACEBOOK_API_VERSION = "v10.0"

FACEBOOK_API_FIELDS = [
    "id",
    "ad_creation_time",
    "ad_creative_body",
    "ad_creative_link_caption",
    "ad_creative_link_description",
    "ad_creative_link_title",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "currency",
    "demographic_distribution",
    "funding_entity",
    "impressions",
    "page_id",
    "potential_reach",
    "region_distribution",
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
FIRST_DATE = date(year=2020, month=1, day=1)
NUMBER_OF_DATES = (date.today() - FIRST_DATE).days + 1

CURRENCY_TO_EUR_MAP = {
    "EUR": 1,
    "USD": 0.83,
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

REGIONS = [
    "drenthe",
    "flevoland",
    "friesland",
    "gelderland",
    "groningen",
    "limburg",
    "noord-brabant",
    "noord-holland",
    "overijssel",
    "utrecht",
    "zeeland",
    "zuid-holland",
]

GENDERS = ["male", "female"]

AGE_RANGES = [
    "13-17",
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-64",
    "65+",
]

IGNORED_WORDS = [
    "productdescription",
    "productbrand",
    "product",
    "brand",
    "description",
    "https",
    "voor",
    "gaan",
    "deze",
    "zijn",
    "over",
    "meer",
    "gaat",
    "weten",
    "keer",
    "onze",
    "word",
    "echt",
    "naar",
    "maar",
    "weer",
    "mensen",
    "ergens",
    "doen",
    "vindt",
    "daarom",
    "worden",
    "moet",
    "niet",
    "partij",
    "stem",
    "maand",
    "vanaf",
    "door",
    "alle",
    "wordt",
    "kunnen",
    "hebben",
    "maken",
    "maart",
    "moeten",
    "heeft",
    "veel",
    "geen",
    "hier",
]
