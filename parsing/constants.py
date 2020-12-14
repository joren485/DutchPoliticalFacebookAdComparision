import os
from datetime import datetime, timedelta

FACEBOOK_API_FIELDS = [
    "currency",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "impressions",
    "page_id",
    "page_name",
    "demographic_distribution",
    "region_distribution",
    "spend",
    "potential_reach",
]

FACEBOOK_API_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_API_URL = (
    f"https://graph.facebook.com/v4.0/ads_archive?"
    f"access_token={FACEBOOK_API_ACCESS_TOKEN}&"
    f"limit=1000&"
    f"fields={','.join(FACEBOOK_API_FIELDS)}&"
    f"search_terms=.&"
    f"ad_reached_countries=NL&"
    f"ad_active_status=all&"
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
    "CDA",
    "CU",
    "D66",
    "DENK",
    "FvD",
    "GL",
    "PVV",
    "PvdA",
    "PvdD",
    "SGP",
    "SP",
    "VVD",
]
REGIONS = [
    "Drenthe",
    "Friesland",
    "Gelderland",
    "Groningen",
    "Limburg",
    "North Brabant",
    "Noord-Holland",
    "Utrecht",
    "Zeeland",
    "Zuid-Holland",
    "Overijssel",
    "Flevoland",
]
GENDERS = ["male", "female"]
AGE_GROUPS = ["13-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
