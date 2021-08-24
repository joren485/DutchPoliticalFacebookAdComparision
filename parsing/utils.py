from datetime import datetime

from typing import Optional, Union

from jinja2 import Environment, FileSystemLoader, select_autoescape

from constants import (
    AGE_RANGES,
    DATA_TYPES,
    DEMOGRAPHIC_TYPES,
    DEMOGRAPHIC_TYPE_TO_LIST_MAP,
    GENDERS,
    PARTIES,
    REGIONS,
    THEMES,
)

JINJA_ENVIRONMENT = Environment(
    loader=FileSystemLoader("../templates"), autoescape=select_autoescape()
)


def recursive_round(o: Union[dict, list], precision: Optional[int] = None) -> None:
    """
    Traverses an object recursively and rounds numbers found in lists.

    :param o: Object to round recursively.
    :param precision: Precision to use when rounding
    """
    if isinstance(o, dict):
        for key in o:
            recursive_round(o[key], 2 if "spend" in key else precision)
    elif isinstance(o, list) and len(o) > 0 and isinstance(o[0], (list, dict)):
        for object_element in o:
            recursive_round(object_element, precision)
    elif isinstance(o, list) and len(o) > 0 and isinstance(o[0], (int, float)):
        for object_index, object_element in enumerate(o):
            o[object_index] = round(object_element, precision)


def render_template(template: str, destination: str, **kwargs) -> None:
    """
    Render a template.

    :param template: The filename of the template.
    :param destination: The filename of the rendered file.
    :param kwargs: Any variables that should be passed to the template.
    :return:
    """

    rendered_content = JINJA_ENVIRONMENT.get_template(template).render(
        last_updated=datetime.now().strftime("%H:%M %d-%m-%Y"),
        PARTIES=PARTIES,
        GENDERS=GENDERS,
        AGE_RANGES=AGE_RANGES,
        REGIONS=REGIONS,
        THEMES=THEMES,
        DATA_TYPES=DATA_TYPES,
        DEMOGRAPHIC_TYPES=DEMOGRAPHIC_TYPES,
        DEMOGRAPHIC_TYPE_TO_LIST_MAP=DEMOGRAPHIC_TYPE_TO_LIST_MAP,
        **kwargs,
    )

    if template == "index.html":
        destination_path = f"../{ destination }"
    else:
        destination_path = f"../website/{ destination }"

    with open(destination_path, "w") as h_destination:
        h_destination.write(rendered_content)
