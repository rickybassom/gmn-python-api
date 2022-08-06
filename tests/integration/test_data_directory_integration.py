"""Integration tests for the GMN Data Directory."""
import unittest

from datetime import datetime
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_summary_reader as msr

class TestDataDirectoryIntergration(unittest.TestCase):
    """Tests for the GMN Data Directory."""

    def test_load_daily_file(self) -> None:
        """
        Test: That get_daily_file_content_by_date can load a daily file from the data directory.
        When: get_daily_file_content_by_date is called.
        """
        trajectory_summary_file_content = dd.get_daily_file_content_by_date(datetime(2022, 5, 28))
        msr.read_meteor_summary_csv_as_dataframe(trajectory_summary_file_content, csv_data_directory_format=True)
