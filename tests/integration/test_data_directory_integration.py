"""Integration tests for the GMN Data Directory."""
import unittest
from datetime import datetime

import requests

from gmn_python_api import data_directory as dd
from gmn_python_api import get_all_file_url
from gmn_python_api import meteor_summary_reader as msr


class TestDataDirectoryIntegration(unittest.TestCase):
    """Tests for live integration with the GMN Data Directory."""

    def test_load_daily_file(self) -> None:
        """
        Test: That read_meteor_summary_csv_as_dataframe can load a daily file from the
         data directory.
        When: get_daily_file_content_by_date is called to fetch  live data from the GMN
         server.
        """
        trajectory_summary_file_content = dd.get_daily_file_content_by_date(
            datetime(2022, 5, 28)
        )
        msr.read_meteor_summary_csv_as_dataframe(
            trajectory_summary_file_content, csv_data_directory_format=True
        )

    def test_load_monthly_file(self) -> None:
        """
        Test: That read_meteor_summary_csv_as_dataframe can load a monthly file from the
         data directory.
        When: get_monthly_file_content_by_date is called to fetch live data from the GMN
         server.
        """
        trajectory_summary_file_content = dd.get_monthly_file_content_by_date(
            datetime(2022, 5, 1)
        )
        msr.read_meteor_summary_csv_as_dataframe(
            trajectory_summary_file_content, csv_data_directory_format=True
        )

    def test_load_all_file_100_lines(self) -> None:
        """
        Test: That read_meteor_summary_csv_as_dataframe can load the first 100 lines of
         the all file from the data
         directory.
        When: get_all_file_url is fetched from the live GMN server.
        """
        r = requests.get(get_all_file_url(), stream=True)

        lines = []
        for line in r.iter_lines():
            lines.append(line.decode("utf-8"))
            if len(lines) == 100:
                break

        msr.read_meteor_summary_csv_as_dataframe(
            "\n".join(lines), csv_data_directory_format=True
        )
