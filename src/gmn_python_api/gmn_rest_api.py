"""
This module contains functions to read data from the GMN REST API.
The REST API uses the Datasette API endpoint. More info:
https://gmn-python-api.readthedocs.io/en/latest/rest_api.html
"""

import json
from urllib.parse import urlencode
import requests
from typing import Optional, Tuple, Iterable, Any, List, Dict

# GMN_REST_API_DOMAIN = "http://0.0.0.0:8001"  # For local testing
GMN_REST_API_DOMAIN = "https://explore.globalmeteornetwork.org"
QUERY_URL = GMN_REST_API_DOMAIN + "/gmn_rest_api?{args}"
METEOR_SUMMARY_QUERY_URL = GMN_REST_API_DOMAIN + "/gmn_rest_api/meteor_summary?{args}"


class LastModifiedError(Exception):
    """
    Raised when the data has modified since the last request.
    """
    pass


def get_meteor_summary_data_all(
        where: Optional[str] = None,
        order_by: Optional[str] = None,
        last_modified_error_retries: int = 3,
) -> List[Dict[str, Any]]:
    """
    Get all meteor summary data from the Meteor Summary GMN REST API endpoint.

    :param where: Optional parameter to filter data via a SQL WHERE clause e.g.
     meteor.unique_trajectory_identifier = '20190103131723_6dnE3'.
    :param order_by: Optional parameter to specify the order of results via a SQL ORDER
     BY clause e.g. meteor.unique_trajectory_identifier DESC.
    :param last_modified_error_retries: Number of times to retry if the data has
     modified since the last request.
    :raises: LastModifiedError: If the data has modified since the last request too many
     times.
    :raises: requests.exceptions.HTTPError: If the HTTP response status code is not 200
     OK.
    :return: A list of json data.
    """
    try_num = 0
    while try_num <= last_modified_error_retries:
        try_num += 1
        try:
            data = []
            for data_iter in get_meteor_summary_data_iter(where, order_by):
                data.extend(data_iter)
        except LastModifiedError:
            # Data has modified since last request, so we need to start from the
            # beginning again.
            continue
        else:
            return data

    raise LastModifiedError("Data has modified since last request too many times.")


def get_meteor_summary_data_iter(
        where: Optional[str] = None,
        order_by: Optional[str] = None,
) -> Iterable[List[Dict[str, Any]]]:
    """
    An iterator for fetching meteor summary data from the Meteor Summary GMN REST API
     endpoint in pages. This is useful for processing large amounts of data. The data is
     returned in pages of 1000 rows.

    :param where: Optional parameter to filter data via a SQL WHERE clause e.g.
     meteor.unique_trajectory_identifier = '20190103131723_6dnE3'.
    :param order_by: Optional parameter to specify the order of results via a SQL ORDER
     BY clause e.g. meteor.unique_trajectory_identifier DESC.
    :raises: requests.exceptions.HTTPError: If the HTTP response status code is not 200
     OK.
    :raises: LastModifiedError: If the data has modified since the last request.
    :raises: requests.exceptions.HTTPError: If the HTTP response status code is not 200
     OK.
    :return: An iterable of json data.
    """
    data, next_url, initial_last_modified = get_meteor_summary_data(where, order_by)
    yield data

    while data and next_url:
        data, next_url, last_modified = get_data_from_url(next_url)
        if last_modified != initial_last_modified:
            raise LastModifiedError("Data has modified since last request.")
        yield data


def get_meteor_summary_data(
        where: Optional[str] = None,
        order_by: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], Optional[str], Optional[str]]:
    """
    Get meteor summary data from the Meteor Summary GMN REST API endpoint starting from
     the first page.

    :param where: Optional parameter to filter data via a SQL WHERE clause e.g.
     meteor.unique_trajectory_identifier = '20190103131723_6dnE3'.
    :param order_by: Optional parameter to specify the order of results via a SQL ORDER
     BY clause e.g. meteor.unique_trajectory_identifier DESC.
    :raises: requests.exceptions.HTTPError: If the HTTP response status code is not 200
     OK.
    :return: Tuple of json data, next URL for pagination, and the last modified date of
     the GMN data store. If iterating through pages, last_modified should be checked
     against the last_modified of the previous page. If they are different, then the
     data has modified since the last request, and the pagination is invalid.
    """
    args = {
        "page": 1,
        "data_format": "json",
        "data_shape": "objects",
    }

    if order_by:
        args["order_by"] = order_by
    if where:
        args["where"] = where

    query_url = METEOR_SUMMARY_QUERY_URL.format(args=urlencode(args))
    return get_data_from_url(query_url)


def get_data(sql: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Get data from the General GMN REST API endpoint using a custom SQL query.

    :param sql: SQL query to execute (read-only).
    :raises: requests.exceptions.HTTPError: If the HTTP response status code is not 200
     OK.
    :return: Tuple containing a list of dictionaries containing meteor trajectory data
     and the last modified date of the GMN data store. If iterating through pages,
     last_modified should be checked against the last_modified of the previous page. If
     they are different, then the data has modified since the last request, and the
     pagination is invalid.
    """
    data, _, last_modified = get_data_from_url(
        QUERY_URL.format(args=urlencode({
            "sql": sql,
            "data_format": "json",
            "data_shape": "objects",
        }))
    )

    return data, last_modified


def get_data_from_url(query_url: str) -> Tuple[List[Dict[str, Any]],
                                               Optional[str], Optional[str]]:
    """
    Get data from a specified GMN REST API endpoint URL.

    :param query_url: URL for querying data from the GMN REST API.
    :raises: requests.exceptions.HTTPError: If the HTTP response status code is not 200
     OK.
    :return: Tuple of json data, next URL for pagination, and the last modified date of
     the GMN data store. If iterating through pages, last_modified should be checked
     against the last_modified of the previous page. If they are different, then the
     data has modified since the last request, and the pagination is invalid.
    """
    data, next_page, gmn_data_store_last_modified = _http_get_response(query_url)

    data_json = json.loads(data)
    if data_json.get("ok"):
        return data_json.get("rows"), next_page, gmn_data_store_last_modified
    else:
        raise ValueError(data_json.get("error"))


def _http_get_response(url: str) -> Tuple[str, Optional[str], Optional[str]]:
    """
    Perform an HTTP GET request and return the response.

    :param url: URL for the HTTP GET request.
    :raises: requests.exceptions.HTTPError: If the HTTP response status code is not 200
     OK.
    :return: Tuple containing the response text, the next URL for pagination, and the
     last modified date of the GMN data store.
    """
    response = requests.get(url, timeout=200, allow_redirects=True)

    try:
        next_url = GMN_REST_API_DOMAIN + response.links.get("next").get(  # type: ignore
            "url")
    except AttributeError:
        next_url = None

    try:
        gmn_data_store_last_modified = response.headers.get("last-modified")
    except AttributeError:
        gmn_data_store_last_modified = None

    if response.ok:
        return str(response.text), next_url, gmn_data_store_last_modified
    else:
        response.raise_for_status()
        return "", None, None
