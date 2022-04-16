"""
This module contains functions to read meteor summary data from the GMN REST API.
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
"""URL template of GMN REST API endpoint."""


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
) -> Tuple[str, str]:
    """
    Get the data from the GMN REST API in a format that is compatible with the
     meteor_summary_csv_reader functions.
    :param where_sql: An optional SQL where clause to filter the data.
    :return: The data from the GMN REST API in CSV format.
    """
    return get_meteor_summary_data(
        table_arguments={"_where": where_sql} if where_sql else None,
        data_format=DataFormat.CSV,
        data_shape=DataShape.ARRAY,
    )


def get_meteor_summary_data(
    table_arguments: Dict[str, str] = None,
    data_format: DataFormat = DataFormat.JSON,
    data_shape: DataShape = DataShape.ARRAY,
) -> Tuple[str, str]:
    """
    Get the data from the GMN REST API.
    :param table_arguments: An optional dictionary of arguments to filter the data.
    :param data_format: The data format of the data.
    :param data_shape: The data shape of the data.
    :return: The data from the GMN REST API.
    """
    return get_data(
        table="meteor_summary",
        table_arguments=table_arguments,
        data_format=data_format,
        data_shape=data_shape,
    )


def get_data_with_sql(
    sql: str,
    data_format: DataFormat = DataFormat.JSON,
    data_shape: DataShape = DataShape.ARRAY,
) -> Tuple[str, str]:
    """
    Get the data from the GMN REST API using an SQL query.
    :param sql: The SQL query to perform against the open access gmn data store database.
    :param data_format: The data format of the data.
    :param data_shape: The data shape of the data.
    :return: The data from the GMN REST API.
    """
    return get_data(
        table_arguments={"sql": sql}, data_format=data_format, data_shape=data_shape
    )


def get_data(
    table: str = None,
    table_arguments: Dict[str, str] = None,
    data_format: DataFormat = DataFormat.JSON,
    data_shape: DataShape = DataShape.OBJECTS,
) -> Tuple[str, str]:
    """
    Get the data from the GMN REST API.
    :param table: The table to query.
    :param table_arguments: An optional dictionary of arguments to filter the data.
    :param data_format: The data format of the data.
    :param data_shape: The data shape of the data.
    :return: The data from the GMN REST API.
    """
    if table_arguments is None:
        table_arguments = {}
    query_url = QUERY_URL.format(
        table="/" + table if table else None,
        data_format=data_format.value,
        data_shape=data_shape.value,
    )
    query_url += "&" + urlencode(table_arguments)
    data = _http_get_response(query_url)
    return data


def _http_get_response(url: str) -> Tuple[str, str]:
    """
    Get the resultant data from a given GMN Data Store REST API URL.

    :param url: The URL of the trajectory summary file.

    :return: The content of the file and an url to access more paginated data if needed.
    :raises: requests.HTTPError If the file url doesn't return a 200 response.
    """
    response = requests.get(url)
    if response.ok:
        try:
            next_url = response.links.get("next").get("url")
        except AttributeError:
            next_url = None
        return str(response.text), next_url
    else:
        response.raise_for_status()
        return "", ""  # pragma: no cover
