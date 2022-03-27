"""
The module contains functions for retrieving IAU meteor shower information.
"""
from typing import Dict

import requests

IAU_SHOWERS_LIST_URL = "https://www.ta3.sk/IAUC22DB/MDC2007/Etc/streamfulldata.txt"
"""The url that contains the list of IAU shower information."""


def get_iau_showers() -> Dict[str, Dict[str, str]]:
    """
    Gets the official list of IAU shower numbers, codes and names.
    :return: A dictionary, where the key is the shower number, of dictionaries
    containing the IAU shower information.
    :raises: requests.HTTPError if the source server doesn't return a 200 response.
    """
    response = requests.get(IAU_SHOWERS_LIST_URL)
    if not response.ok:
        response.raise_for_status()
        return {}  # pragma: no cover

    showers = {}
    for row in response.text.splitlines():
        if not row or row.startswith(":") or row.startswith("+"):
            continue

        row_values = row.split("|")

        shower_no = row_values[1].strip('" ')
        if shower_no in showers:
            continue

        shower_code = row_values[3].strip('" ')
        shower_name = row_values[4].strip('" ')

        showers[shower_no] = {"id": shower_no, "code": shower_code, "name": shower_name}

    return showers
