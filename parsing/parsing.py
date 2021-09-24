import logging
from datetime import datetime
from decimal import Decimal
from typing import Optional, Tuple

from constants import (
    AGE_RANGES,
    CURRENCY_EXCHANGE_RATE_MAP,
    DATETIME_FORMAT,
    GENDER_IGNORE_LIST,
    GENDERS,
    REGION_IGNORE_LIST,
    REGIONS,
)
from models import Ad


def _parse_date(data: dict, key: str) -> Optional[datetime]:
    return datetime.strptime(data[key], DATETIME_FORMAT) if key in data else None


def _parse_estimated_value(data: dict, key: str) -> Tuple[int, int]:
    if key not in data:
        return 0, 0

    lower = int(data[key]["lower_bound"])
    upper = int(data[key]["upper_bound"]) if "upper_bound" in data[key] else lower
    return lower, upper


def _parse_content(data: dict, key: str):
    if key not in data:
        return ""

    return " ".join(
        set(
            filter(
                lambda s: not s.startswith(("{{product", "{{ngMeta")),
                data[key],
            )
        )
    )


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
        "creative_bodies": _parse_content(ad_json_data, "ad_creative_bodies"),
        "creative_link_captions": _parse_content(
            ad_json_data, "ad_creative_link_captions"
        ),
        "creative_link_descriptions": _parse_content(
            ad_json_data, "ad_creative_link_descriptions"
        ),
        "creative_link_titles": _parse_content(ad_json_data, "ad_creative_link_titles"),
        "spending_lower": spending_lower,
        "spending_upper": spending_upper,
        "impressions_lower": impressions_lower,
        "impressions_upper": impressions_upper,
        "potential_reach_lower": potential_reach_lower,
        "potential_reach_upper": potential_reach_upper,
    }

    if "languages" in ad_json_data and ad_json_data["languages"] != ["nl"]:
        logging.warning(
            f"Non-dutch language detected "
            f"({ad_dict['ad_id']}): {','.join(ad_json_data['languages'])}"
        )

    if "delivery_by_region" in ad_json_data:
        for distribution in ad_json_data["delivery_by_region"]:
            region = distribution["region"]
            percentage = Decimal(distribution["percentage"])
            if region == "North Brabant":
                region = "Noord-Brabant"

            if region in REGIONS:
                field_name = Ad.demographic_to_field_name(region)
                ad_dict[field_name] = percentage
            else:
                if region not in REGION_IGNORE_LIST:
                    logging.warning(f"Unknown region: {region} ({ad_dict['ad_id']})")

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
                    if demographic not in GENDER_IGNORE_LIST:
                        logging.warning(
                            f"Unknown gender/age group: "
                            f"{demographic} ({ad_dict['ad_id']})"
                        )

    return ad_dict
