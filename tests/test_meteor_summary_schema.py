"""Tests for trajectory_summary_schema.py module"""
import unittest
from unittest import mock

import pandas as pd  # type: ignore

from gmn_python_api import meteor_summary_schema


class Test(unittest.TestCase):
    """Tests for the meteor_summary_schema module."""

    @mock.patch(
        "gmn_python_api.meteor_summary_schema."
        "gmn_python_api.read_meteor_summary_csv_as_dataframe"
    )
    def test_get_meteor_summary_csv_avro_schema(
        self, mock_data_frame: mock.Mock
    ) -> None:
        """
        Test: That get_trajectory_summary_avro_schema returns the correct schema.
        When: get_trajectory_summary_avro_schema() is called with a mocked trajectory
         summary data frame.
        """
        expected_data_frame = pd.DataFrame(
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
        mock_data_frame.return_value = expected_data_frame

        expected_schema = {
            "type": "record",
            "name": "Root",
            "fields": [
                {"name": "trajectory_id", "type": ["null", "long"]},
                {"name": "trajectory_start_time", "type": ["null", "double"]},
                {"name": "trajectory_end_time", "type": ["null", "double"]},
                {"name": "iau_code", "type": ["null", "string"]},
                {"name": "schema_version", "type": ["null", "string"]},
                {
                    "name": "trajectory_participating_stations",
                    "type": ["null", {"type": "array", "items": ["null", "string"]}],
                },
            ],
        }
        actual_schema = meteor_summary_schema.get_meteor_summary_avro_schema()
        self.assertEqual(expected_schema, actual_schema)

    @mock.patch("gmn_python_api.read_meteor_summary_csv_as_dataframe")
    def test_get_verbose_and_camel_case_column_name_bidict(
        self, mock_read_meteor_summary_csv_as_dataframe: mock.Mock
    ):
        """
        Test: get_verbose_and_camel_case_column_name_bidict produces correct dictionary.
        When: get_verbose_and_camel_case_column_name_bidict is called with mocked dataframes.
        """
        verbose_data_frame = pd.DataFrame(
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
        verbose_data_frame.set_index("Trajectory (Id)", inplace=True)

        camel_case_data_frame = pd.DataFrame(
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
        camel_case_data_frame.set_index("trajectory_id", inplace=True)

        mock_read_meteor_summary_csv_as_dataframe.side_effect = [
            verbose_data_frame,
            camel_case_data_frame,
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
