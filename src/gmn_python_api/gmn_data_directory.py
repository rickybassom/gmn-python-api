"""This module contains the code to read from the GMN data directory."""
from datetime import datetime
from typing import List
from typing import Optional

import requests
from bs4 import BeautifulSoup  # type: ignore

GMN_DATA_DIRECTORY_BASE_URL: str = (
    "https://globalmeteornetwork.org/data/traj_summary_data/"
)
GMN_DATA_START_DATE: datetime = datetime(2018, 1, 9)
SUMMARY_YESTERDAY_FILENAME: str = "traj_summary_yesterday.txt"
SUMMARY_TODAY_FILENAME: str = "traj_summary_latest_daily.txt"


class GmnDataDirectory:
    """Methods to read from the GMN data directory."""

    def __init__(self, base_url: str = GMN_DATA_DIRECTORY_BASE_URL):
        """
        :param base_url: (Optional str) The base URL of the GMN data directory. Defaults to GMN_DATA_DIRECTORY_BASE_URL.
        """
        self.base_url: str = base_url
        self.summary_yesterday_filename: str = SUMMARY_YESTERDAY_FILENAME
        self.summary_today_filename: str = SUMMARY_TODAY_FILENAME

    def get_all_daily_file_urls(self) -> List[str]:
        """
        Get all daily file urls from the GMN data directory.
        :return: (List[str]) A list of all daily filenames.
        :raises: (requests.HTTPError) If the data directory url doesn't return a 200 response.
        """
        return _get_url_paths(self.base_url + "daily/", "txt")

    def get_all_monthly_file_urls(self) -> List[str]:
        """
        Get all monthly file urls from the GMN data directory.
        :return: (List[str]) A list of all monthly filenames.
        :raises: (requests.HTTPError) If the data directory url doesn't return a 200 response.
        """
        return _get_url_paths(self.base_url + "monthly/", "txt")

    def get_daily_file_url_by_date(
        self, date: datetime, current_date: Optional[datetime] = None
    ) -> str:
        """
        Get the URL of the daily file for a given date.
        :param date: (datetime) The date to get the daily file for.
        :param current_date: (Optional datetime) The current date. Defaults to datetime.now().
        :return: (str) The URL of the daily file.
        :raises: (requests.HTTPError) If the data directory url doesn't return a 200 response.
        """
        if not current_date:
            current_date = datetime.today()

        if date == current_date:
            return self.base_url + "daily/" + SUMMARY_TODAY_FILENAME

        if date.day == current_date.day - 1:
            return self.base_url + "daily/" + SUMMARY_YESTERDAY_FILENAME

        all_daily_filenames = self.get_all_daily_file_urls()
        files_containing_date = [
            f for f in all_daily_filenames if date.strftime("%Y%m%d") in f
        ]
        return files_containing_date[0]

    def get_monthly_file_url_by_month(self, date: datetime) -> str:
        """
        Get the URL of the monthly file for a given month.
        :param date: (datetime) The date to get the monthly file for.
        :return: (str) The URL of the monthly file.
        :raises: (requests.HTTPError) If the data directory url doesn't return a 200 response.
        """
        all_monthly_filenames = self.get_all_monthly_file_urls()
        files_containing_date = [
            f for f in all_monthly_filenames if date.strftime("%Y%m") in f
        ]
        return files_containing_date[0]

    def get_daily_file_content_by_date(
        self, date: datetime, current_date: Optional[datetime] = None
    ) -> str:
        """
        Get the content of the daily trajectory summary file for a given date.
        :param date: (datetime) The date to get the daily file for.
        :param current_date: (Optional datetime) The current date. Defaults to datetime.now().
        :return: (str) The content of the daily file.
        :raises: (requests.HTTPError) If the data directory url doesn't return a 200 response.
        """
        file_url = self.get_daily_file_url_by_date(date, current_date)

        response = requests.get(file_url)
        if response.ok:
            return str(response.text)
        else:
            response.raise_for_status()
            return ""  # pragma: no cover

    def get_monthly_file_content_by_date(self, date: datetime) -> str:
        """
        Get the content of the monthly trajectory summary file for a given date.
        :param date: (datetime) The date to get the monthly file for.
        :return: (str) The content of the monthly file.
        :raises: (requests.HTTPError) If the data directory url doesn't return a 200 response.
        """
        file_url = self.get_monthly_file_url_by_month(date)

        response = requests.get(file_url)
        if response.ok:
            return str(response.text)
        else:
            response.raise_for_status()
            return ""  # pragma: no cover


def _get_url_paths(url: str, ext: str = "") -> List[str]:
    """
    Get all paths from a directory listing URL.
    :param url: (str) The URL to get the paths from.
    :param ext: (Optional str) The extension to filter by.
    :return: (List[str]) A list of all paths.
    :raises: (requests.HTTPError) If the URL doesn't return a 200 response.
    """
    response = requests.get(url)
    if response.ok:
        response_text = str(response.text)
    else:
        response.raise_for_status()
        return []  # pragma: no cover
    soup = BeautifulSoup(response_text, "html.parser")
    parent = [
        url + node.get("href")
        for node in soup.find_all("a")
        if node.get("href").endswith(ext)
    ]
    return parent
