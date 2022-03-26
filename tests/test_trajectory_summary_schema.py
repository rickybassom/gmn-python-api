"""Tests for trajectory_summary_schema.py module"""
import unittest
from unittest import mock

import pandas as pd

from gmn_python_api import trajectory_summary_schema


class Test(unittest.TestCase):
    """Tests for the trajectory_summary_schema module."""

    @mock.patch(
        "gmn_python_api.trajectory_summary_schema."
        "gmn_python_api.read_trajectory_summary_as_dataframe"
    )
    def test_get_trajectory_summary_avro_schema(
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
        # expected_data_frame.index.name = "trajectory_id"
        # Set index column
        expected_data_frame.set_index("trajectory_id", inplace=True)
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
        actual_schema = trajectory_summary_schema.get_trajectory_summary_avro_schema()
        self.assertEqual(expected_schema, actual_schema)
