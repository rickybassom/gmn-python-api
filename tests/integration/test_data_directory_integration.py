"""Integration tests for the GMN Data Directory."""
import unittest
from datetime import date

import requests

from gmn_python_api import data_directory as dd
from gmn_python_api.data_directory import DAILY_DATE_INPUT_FORMAT, \
    MONTHLY_DATE_INPUT_FORMAT
from gmn_python_api import meteor_summary_reader as msr


class TestDataDirectoryIntegration(unittest.TestCase):
    """Tests for live integration with the GMN Data Directory."""

    def test_load_today_daily_file(self) -> None:
        """
        Test: That read_meteor_summary_csv_as_dataframe can load a today's daily file
         from the data directory.
        When: get_daily_file_content_by_date is called to fetch live data from the GMN
         server.
        """
        trajectory_summary_file_content = dd.get_daily_file_content_by_date(
            date.today().strftime(DAILY_DATE_INPUT_FORMAT))
        msr.read_meteor_summary_csv_as_dataframe(trajectory_summary_file_content)

    def test_load_daily_file(self) -> None:
        """
        Test: That read_meteor_summary_csv_as_dataframe can load a daily file from the
         data directory.
        When: get_daily_file_content_by_date is called to fetch live data from the GMN
         server.
        """
        trajectory_summary_file_content = dd.get_daily_file_content_by_date(
            date(2018, 12, 10).strftime(DAILY_DATE_INPUT_FORMAT)
        )
        msr.read_meteor_summary_csv_as_dataframe(trajectory_summary_file_content)

    def test_load_monthly_file(self) -> None:
        """
        Test: That read_meteor_summary_csv_as_dataframe can load a monthly file from the
         data directory.
        When: get_monthly_file_content_by_date is called to fetch live data from the GMN
         server.
        """
        trajectory_summary_file_content = dd.get_monthly_file_content_by_date(
            date(2019, 1, 1).strftime(MONTHLY_DATE_INPUT_FORMAT)
        )
        msr.read_meteor_summary_csv_as_dataframe(trajectory_summary_file_content)

    def test_load_all_file_100_lines(self) -> None:
        """
        Test: That read_meteor_summary_csv_as_dataframe can load the first 100 lines of
         the all file from the data directory.
        When: get_all_file_url is fetched from the live GMN server.
        """
        r = requests.get(dd.get_all_file_url(), stream=True, timeout=200)

        lines = []
        for line in r.iter_lines():
            lines.append(line.decode("utf-8"))
            if len(lines) == 100:
                break

        msr.read_meteor_summary_csv_as_dataframe("\n".join(lines))


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
