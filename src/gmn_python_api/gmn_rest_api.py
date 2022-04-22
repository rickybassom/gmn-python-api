"""
This module contains functions to read meteor summary data from the GMN REST API.
 The REST API uses the Datasette API endpoint. More info:
 https://docs.datasette.io/en/stable/json_api.html
"""
from enum import Enum
from typing import Dict
from typing import Optional
from typing import Tuple
from urllib.parse import urlencode

import requests

QUERY_URL = (
    "https://globalmeteornetwork.org/gmn_data_store"
    "{table}.{data_format}?_shape={data_shape}"
)
"""
URL template of GMN REST API endpoint. Note that the GMN REST API currently isn't live,
 so this URL should be replaced with a local instance of the GMN REST API to use
 functions in this module (e.g
 http:0.0.0.0:8001/gmn_data_store{table}.{data_format}?_shape={data_shape}).
"""


class DataFormat(str, Enum):
    """REST data format."""

    JSON = "json"
    CSV = "csv"


class DataShape(str, Enum):
    """REST data shape."""

    ARRAYS = "arrays"
    OBJECTS = "objects"
    ARRAY = "array"
    OBJECT = "object"


def get_meteor_summary_data_reader_compatible(
    where_sql: Optional[str] = None,
    next_page: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """
    Get meteor summary data from the GMN REST API in a format that is compatible with
     the meteor_summary_reader functions.

    :param where_sql: An optional SQL WHERE clause to filter the data (e.g. iau_no='4').
    :param next_page: An optional URL to access more paginated data provided by the api.

    :return: The data returned from the GMN REST API in CSV format.
    :raises: requests.HTTPError If GMN REST API doesn't return a 200 response.
    """
    return get_meteor_summary_data(
        table_arguments={"_where": where_sql} if where_sql else None,
        data_format=DataFormat.CSV,
        data_shape=DataShape.ARRAY,
        next_page=next_page,
    )


def get_meteor_summary_data(
    table_arguments: Optional[Dict[str, str]] = None,
    data_format: DataFormat = DataFormat.JSON,
    data_shape: DataShape = DataShape.ARRAY,
    next_page: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """
    Get meteor summary data from the GMN REST API.

    :param table_arguments: An optional dictionary of arguments to filter the data.
     A full list of arguments can be found here:
     https://docs.datasette.io/en/stable/json_api.html#table-arguments
    :param data_format: The data format of the meteor summary data using DataFormat
     enum.
    :param data_shape: The data shape of the meteor summary data using the DataShape
     enum.
    :param next_page: An optional URL to access more paginated data provided by the api.

    :return: The data returned from the GMN REST API.
    :raises: requests.HTTPError If GMN REST API doesn't return a 200 response.
    """
    return get_data(
        table="meteor_summary",
        table_arguments=table_arguments,
        data_format=data_format,
        data_shape=data_shape,
        next_page=next_page,
    )


def get_data_with_sql(
    sql: str,
    data_format: DataFormat = DataFormat.JSON,
    data_shape: DataShape = DataShape.ARRAY,
    next_page: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """
    Get any available data from the GMN REST API using a readonly SQL query.

    :param sql: The SQL query to perform against the open access GMN Data Store database.
    :param data_format: The data format of the data using the DataFormat enum.
    :param data_shape: The data shape of the data using the DataShape enum.
    :param next_page: An optional URL to access more paginated data provided by the api.

    :return: The data returned from the GMN REST API.
    :raises: requests.HTTPError If GMN REST API doesn't return a 200 response.
    """
    return get_data(
        table_arguments={"sql": sql},
        data_format=data_format,
        data_shape=data_shape,
        next_page=next_page,
    )


def get_data(
    table: Optional[str] = None,
    table_arguments: Optional[Dict[str, str]] = None,
    data_format: DataFormat = DataFormat.JSON,
    data_shape: DataShape = DataShape.OBJECTS,
    next_page: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """
    Get any data from the GMN REST API.

    :param table: The table to query in the GMN Data Store.
    :param table_arguments: An optional dictionary of arguments to filter the data. A
     full list of arguments can be found here:
     https://docs.datasette.io/en/stable/json_api.html#table-arguments
    :param data_format: The data format of the data using the DataFormat enum.
    :param data_shape: The data shape of the data using the DataShape enum.

    :return: The data returned from the GMN REST API.
    :raises: requests.HTTPError If GMN REST API doesn't return a 200 response.
    """
    if table_arguments is None:
        table_arguments = {}

    if next_page:
        query_url = next_page
    else:
        query_url = QUERY_URL.format(
            table="/" + table if table else None,
            data_format=data_format.value,
            data_shape=data_shape.value,
        )
        query_url += "&" + urlencode(table_arguments)

    data = _http_get_response(query_url)
    return data


def _http_get_response(url: str) -> Tuple[str, Optional[str]]:
    """
    Get resultant data from a given GMN REST API URL.

    :param url: A query URL of the GMN REST API.

    :return: Data, and a URL to access more paginated data if required.
    :raises: requests.HTTPError If URL doesn't return a 200 response.
    """
    response = requests.get(url)
    if response.ok:
        try:
            next_url = response.links.get("next").get("url")  # type: ignore
        except AttributeError:
            # next_url somtimes is not given even when paginated (for example with CSVs)
            if str(response.text).count("\n") == 101 and (
                requests.head(url + "&_next=100").ok
                or requests.head(url + "?_next=100").ok
            ):  # pragma: no cover
                next_url = url + "&_next=100" if "?" in url else url + "?_next=100"
            else:
                next_url = None
        return str(response.text), next_url
    else:
        response.raise_for_status()
        return "", ""  # pragma: no cover
