"""Tests for trajectory_summary_schema module"""
import unittest
from unittest import mock

import pandas as pd  # type: ignore

from gmn_python_api import meteor_summary_schema

TEST_VERBOSE_DATAFRAME = pd.DataFrame(
    {
        "Trajectory (Id)": [1, 2, 3],
        "Trajectory Start Time": [1.123, 2.5423, 3.343],
        "Trajectory End Time": [2.123, 3.5423, 4.343],
        "IAU Code": ["trajectory_1", "trajectory_2", "trajectory_3"],
        "Schema Version": ["1.0", "1.0", "1.0"],
        "Trajectory Participating Stations": [
            ["station_1", "station_2"],
            ["station_3", "station_4"],
            ["station_5", "station_6"],
        ],
    }
)
TEST_VERBOSE_DATAFRAME.set_index("Trajectory (Id)", inplace=True)

TEST_CAMEL_CASE_DATAFRAME = pd.DataFrame(
    {
        "trajectory_id": [1, 2, 3],
        "trajectory_start_time": [1.123, 2.5423, 3.343],
        "trajectory_end_time": [2.123, 3.5423, 4.343],
        "iau_code": ["trajectory_1", "trajectory_2", "trajectory_3"],
        "schema_version": ["1.0", "1.0", "1.0"],
        "trajectory_participating_stations": [
            ["station_1", "station_2"],
            ["station_3", "station_4"],
            ["station_5", "station_6"],
        ],
    }
)
TEST_CAMEL_CASE_DATAFRAME.set_index("trajectory_id", inplace=True)


class TestMeteorSummarySchema(unittest.TestCase):
    """Tests for the meteor_summary_schema module."""

    @mock.patch("gmn_python_api.meteor_summary_reader.read_meteor_summary_csv_as_dataframe")
    def test_get_column_names(self,
                              mock_read_meteor_summary_csv_as_dataframe: mock.Mock) -> None:
        """
        Test: get_column_names returns correct column names.
        When: get_column_names is called with mocked model dataframe.
        """
        mock_read_meteor_summary_csv_as_dataframe.side_effect = [
            TEST_VERBOSE_DATAFRAME,
            TEST_CAMEL_CASE_DATAFRAME,
        ]

        self.assertEqual(
            meteor_summary_schema.get_column_names(camel_case=True),
            [
                "Trajectory (Id)",
                "Trajectory Start Time",
                "Trajectory End Time",
                "IAU Code",
                "Schema Version",
                "Trajectory Participating Stations",
            ],
        )
        self.assertEqual(
            meteor_summary_schema.get_column_names(camel_case=False),
            [
                "trajectory_id",
                "trajectory_start_time",
                "trajectory_end_time",
                "iau_code",
                "schema_version",
                "trajectory_participating_stations",
            ],
        )

    def test_get_model_meteor_summary_dataframe(self) -> None:
        """
        Test: get_model_meteor_summary_dataframe returns non empty dataframe.
        When: get_model_meteor_summary_dataframe is called.
        """
        dataframe_no_camelcase = meteor_summary_schema.get_model_meteor_summary_dataframe(
            camel_case=False,
        )
        dataframe_camelcase = meteor_summary_schema.get_model_meteor_summary_dataframe(
            camel_case=True,
        )

        self.assertFalse(dataframe_no_camelcase.empty)
        self.assertFalse(dataframe_camelcase.empty)

    @mock.patch("gmn_python_api.read_meteor_summary_csv_as_dataframe")
    def test_get_verbose_and_camel_case_column_name_bidict(
            self, mock_read_meteor_summary_csv_as_dataframe: mock.Mock
    ) -> None:
        """
        Test: get_verbose_and_camel_case_column_name_bidict produces correct dictionary.
        When: get_verbose_and_camel_case_column_name_bidict is called with mocked dataframes.
        """
        mock_read_meteor_summary_csv_as_dataframe.side_effect = [
            TEST_VERBOSE_DATAFRAME,
            TEST_CAMEL_CASE_DATAFRAME,
        ]

        expected_bidict = {
            "Trajectory (Id)": "trajectory_id",
            "trajectory_id": "Trajectory (Id)",
            "Trajectory Start Time": "trajectory_start_time",
            "trajectory_start_time": "Trajectory Start Time",
            "Trajectory End Time": "trajectory_end_time",
            "trajectory_end_time": "Trajectory End Time",
            "IAU Code": "iau_code",
            "iau_code": "IAU Code",
            "Schema Version": "schema_version",
            "schema_version": "Schema Version",
            "Trajectory Participating Stations": "trajectory_participating_stations",
            "trajectory_participating_stations": "Trajectory Participating Stations",
        }

        actual_bidict = (
            meteor_summary_schema.get_verbose_and_camel_case_column_name_bidict()
        )
        self.assertEqual(expected_bidict, actual_bidict)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
