import os
from datetime import datetime, timedelta

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
    "ad_snapshot_url",
    "currency",
    "demographic_distribution",
    "funding_entity",
    "impressions",
    "page_id",
    "page_name",
    "potential_reach",
    "publisher_platforms",
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
FIRST_DATE = datetime(year=2020, month=1, day=1)
DATES = [date for date in (FIRST_DATE + timedelta(days=n) for n in range((datetime.today() - FIRST_DATE).days + 1))]

CURRENCY_TO_EUR_MAP = {
    "EUR": 1,
    "USD": 0.83,
}

PARTIES = [
    "50P",
    "BIJ1",
    "BBB",
    "CDA",
    "CU",
    "CO",
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

FACEBOOK_REGION_TO_REGION_MAP = {
    "Drenthe": "Drenthe",
    "Friesland": "Friesland",
    "Gelderland": "Gelderland",
    "Groningen": "Groningen",
    "Limburg": "Limburg",
    "North Brabant": "Noord-Brabant",
    "Noord-Brabant": "Noord-Brabant",
    "Noord-Holland": "Noord-Holland",
    "Utrecht": "Utrecht",
    "Zeeland": "Zeeland",
    "Zuid-Holland": "Zuid-Holland",
    "Overijssel": "Overijssel",
    "Flevoland": "Flevoland",
}
REGIONS = list(set(FACEBOOK_REGION_TO_REGION_MAP.values()))

FACEBOOK_GENDER_TO_GENDER_MAP = {"male": "Male", "female": "Female"}
GENDERS = list(set(FACEBOOK_GENDER_TO_GENDER_MAP.values()))

FACEBOOK_AGE_TO_AGE_MAP = {
    "13-17": "13-17",
    "18-24": "18-24",
    "25-34": "25-34",
    "35-44": "35-44",
    "45-54": "45-54",
    "55-64": "55-64",
    "65+": "65+",
}
AGES = list(set(FACEBOOK_AGE_TO_AGE_MAP.values()))
