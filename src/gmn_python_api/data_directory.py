"""
This module contains functions to read trajectory summary files from the GMN data
directory.
"""
from datetime import date, datetime
from datetime import timedelta
from typing import List
from typing import Optional

import requests
from bs4 import BeautifulSoup  # type: ignore

BASE_URL: str = "https://globalmeteornetwork.org/data/traj_summary_data/"
"""The base URL for trajectory summary files in the GMN data directory."""

DATA_START_DATE: date = date(2018, 12, 9)
"""The date of the earliest trajectory summary file in the GMN data directory."""

DAILY_DIRECTORY: str = "daily/"
"""The name of the directory containing daily trajectory summary files in the
base URL."""

MONTHLY_DIRECTORY: str = "monthly/"
"""The name of the directory containing monthly trajectory summary files in
# the base URL."""

SUMMARY_FILE_EXTENSION: str = "txt"
"""The extension of the trajectory summary files in the GMN data directory"""

SUMMARY_TODAY_FILENAME: str = "traj_summary_latest_daily.txt"
"""The filename of the most recent trajectory summary file."""

SUMMARY_YESTERDAY_FILENAME: str = "traj_summary_yesterday.txt"
"""The filename of the trajectory summary file from yesterday."""

SUMMARY_ALL_FILENAME: str = "traj_summary_all.txt"
"""The filename of the trajectory summary file containing all data."""

DAILY_DATE_INPUT_FORMAT: str = "%Y-%m-%d"
"""The daily string date format that should be passed into the functions in this."""

MONTHLY_DATE_INPUT_FORMAT: str = "%Y-%m"
"""The monthly string date format that should be passed into the functions in this."""


def get_all_daily_file_urls() -> List[str]:
    """
    Get all daily trajectory summary file urls from the GMN data directory.

    :return: A list of all daily file urls.
    :raises: requests.HTTPError if the data directory url doesn't return a 200 response.
    """
    return _get_url_paths(BASE_URL + DAILY_DIRECTORY, SUMMARY_FILE_EXTENSION)


def get_all_monthly_file_urls() -> List[str]:
    """
    Get all monthly trajectory summary file urls from the GMN data directory.

    :return: A list of all monthly file urls.
    :raises: requests.HTTPError if the data directory url doesn't return a 200 response.
    """
    return _get_url_paths(BASE_URL + MONTHLY_DIRECTORY, SUMMARY_FILE_EXTENSION)


def get_all_file_url() -> str:
    """
    Get the URL of the trajectory summary file containing all data.

    :return: The URL of the file containing all data.
    """
    return BASE_URL + SUMMARY_ALL_FILENAME


def get_daily_file_url_by_date(
        date_str: str, current_date: Optional[date] = None
) -> str:
    """
    Get the URL of the daily trajectory summary file for a given date.

    :param date_str: The date of the daily file to get in the format YYYY-MM-DD.
    :param current_date: The current date. Defaults to datetime.now().

    :return: The URL of the daily file.
    :raises: FileNotFoundError if the daily file cannot be found. Or
     requests.HTTPError is raised if the file url doesn't return a 200 response.
    """
    date = datetime.strptime(date_str, DAILY_DATE_INPUT_FORMAT).date()

    if not current_date:
        current_date = datetime.today().date()
    else:
        current_date = current_date

    if date == current_date:
        return BASE_URL + DAILY_DIRECTORY + SUMMARY_TODAY_FILENAME

    if date == current_date - timedelta(days=1):
        return BASE_URL + DAILY_DIRECTORY + SUMMARY_YESTERDAY_FILENAME

    all_daily_filenames = get_all_daily_file_urls()
    files_containing_date = [
        f for f in all_daily_filenames if date.strftime("%Y%m%d") in f
    ]

    if len(files_containing_date) == 0:
        raise FileNotFoundError(f"Trajectory summary file not found for date "
                                f"{date.strftime(DAILY_DATE_INPUT_FORMAT)}")

    return files_containing_date[0]


def get_monthly_file_url_by_month(date_str: str) -> str:
    """
    Get the URL of the monthly trajectory summary file for a given month.

    :param date_str: The date of the monthly file to get in the format YYYY-MM.

    :return: The URL of the monthly file.
    :raises: FileNotFoundError if the monthly file cannot be found. Or
     requests.HTTPError is raised if the file url doesn't return a 200 response.
    """
    date = datetime.strptime(date_str, MONTHLY_DATE_INPUT_FORMAT).date()
    all_monthly_filenames = get_all_monthly_file_urls()
    files_containing_date = [
        f for f in all_monthly_filenames if date.strftime("%Y%m") in f
    ]

    if len(files_containing_date) == 0:
        raise FileNotFoundError(
            f"Trajectory summary file not found for month in date "
            f"{date.strftime(MONTHLY_DATE_INPUT_FORMAT)}"
        )

    return files_containing_date[0]


def get_file_content_from_url(file_url: str) -> str:
    """
    Get the content of a trajectory summary file from a given URL.

    :param url: The URL of the trajectory summary file.

    :return: The content of the file.
    :raises: requests.HTTPError If the file url doesn't return a 200 response.
    """
    response = requests.get(file_url)
    if response.ok:
        return str(response.text)
    else:
        response.raise_for_status()
        return ""  # pragma: no cover


def get_daily_file_content_by_date(
        date_str: str, current_date: Optional[date] = None
) -> str:
    """
    Get the content of the daily trajectory summary file for a given date.

    :param date_str: The date of the daily file to get in the format YYYY-MM-DD.
    :param current_date: The current date. Defaults to datetime.now().

    :return: The content of the daily file.
    :raises: requests.HTTPError if the data directory url doesn't return a 200 response.
    """
    file_url = get_daily_file_url_by_date(date_str, current_date)
    return get_file_content_from_url(file_url)


def get_monthly_file_content_by_date(date_str: str) -> str:
    """
    Get the content of the monthly trajectory summary file for a given date.

    :param date_str: The date to get the monthly file for in the format YYYY-MM.

    :return: The content of the monthly file.
    :raises: requests.HTTPError if the data directory url doesn't return a 200 response.
    """
    file_url = get_monthly_file_url_by_month(date_str)
    return get_file_content_from_url(file_url)


def get_all_file_content() -> str:
    """
    Get the content of the trajectory summary file containing all data.

    :return: The content of the file containing all data.
    :raises: requests.HTTPError if the data directory url doesn't return a 200 response.
    """
    file_url = get_all_file_url()
    return get_file_content_from_url(file_url)


def _get_url_paths(url: str, ext: str = "") -> List[str]:
    """
    Get all paths from a directory listing URL.

    :param url: The URL to get the paths from.
    :param ext: The extension to filter by.

    :return: A list of all paths.
    :raises: requests.HTTPError if the URL doesn't return a 200 response.
    """
    response_text = get_file_content_from_url(url)
    soup = BeautifulSoup(response_text, "html.parser")
    parent = [
        url + node.get("href")
        for node in soup.find_all("a")
        if node.get("href").endswith(ext)
    ]
    return parent
