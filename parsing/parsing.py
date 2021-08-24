import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple

from constants import (
    AGE_RANGES,
    CURRENCY_EXCHANGE_RATE_MAP,
    DATETIME_FORMAT,
    GENDERS,
    REGIONS,
)

from models import Ad

LOGGER = logging.getLogger(__name__)


def _parse_date(data: dict, key: str) -> Optional[datetime]:
    return datetime.strptime(data[key], DATETIME_FORMAT) if key in data else None


def _parse_estimated_value(data: dict, key: str) -> Tuple[int, int]:
    if key not in data:
        return 0, 0

    lower = int(data[key]["lower_bound"])
    upper = int(data[key]["upper_bound"]) if "upper_bound" in data[key] else lower
    return lower, upper


def json_to_ad_dict(ad_json_data: dict, party: str) -> dict:
    """
    Transform a json object into an dictionary that corresponds with the Ad model.

    :param ad_json_data: Json object representing an ad from the Facebook API.
    :param party: Current party to parse.
    :return: A dict corresponds with the Ad model.
    """
    spending_lower, spending_upper = _parse_estimated_value(ad_json_data, "spend")
    spending_lower *= CURRENCY_EXCHANGE_RATE_MAP[ad_json_data["currency"]]
    spending_upper *= CURRENCY_EXCHANGE_RATE_MAP[ad_json_data["currency"]]

    impressions_lower, impressions_upper = _parse_estimated_value(
        ad_json_data, "impressions"
    )
    potential_reach_lower, potential_reach_upper = _parse_estimated_value(
        ad_json_data, "potential_reach"
    )

    ad_dict = {
        "ad_id": ad_json_data["id"],
        "page_id": ad_json_data["page_id"],
        "party": party,
        "creation_date": _parse_date(ad_json_data, "ad_creation_time"),
        "start_date": _parse_date(ad_json_data, "ad_delivery_start_time"),
        "end_date": _parse_date(ad_json_data, "ad_delivery_stop_time"),
        "creative_body": ad_json_data.get("ad_creative_body", ""),
        "creative_link_caption": ad_json_data.get("ad_creative_link_caption", ""),
        "creative_link_description": ad_json_data.get(
            "ad_creative_link_description", ""
        ),
        "creative_link_title": ad_json_data.get("ad_creative_link_title", ""),
        "spending_lower": spending_lower,
        "spending_upper": spending_upper,
        "impressions_lower": impressions_lower,
        "impressions_upper": impressions_upper,
        "potential_reach_lower": potential_reach_lower,
        "potential_reach_upper": potential_reach_upper,
    }

    if "region_distribution" in ad_json_data:
        for distribution in ad_json_data["region_distribution"]:
            region = distribution["region"].lower()
            percentage = Decimal(distribution["percentage"])
            if region == "north brabant":
                region = "noord-brabant"

            if region in REGIONS:
                field_name = Ad.demographic_to_field_name(region)
                ad_dict[field_name] = percentage
            else:
                if region not in ("unknown", "Unknown"):
                    LOGGER.info(f"Unknown: {region} ({percentage})")

    if "demographic_distribution" in ad_json_data:
        for distribution in ad_json_data["demographic_distribution"]:
            percentage = Decimal(distribution["percentage"])
            for demographic in (distribution["gender"], distribution["age"]):
                if demographic in GENDERS or demographic in AGE_RANGES:
                    field_name = Ad.demographic_to_field_name(demographic)
                    if field_name not in ad_dict:
                        ad_dict[field_name] = percentage
                    else:
                        ad_dict[field_name] += percentage
                else:
                    if demographic not in ("unknown", "Unknown"):
                        LOGGER.info(f"Unknown: {demographic} ({percentage})")

    return ad_dict
