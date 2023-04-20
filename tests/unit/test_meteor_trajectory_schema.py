"""Tests for meteor_trajectory_schema module"""
import unittest
from unittest import mock

import pandas as pd  # type: ignore

from gmn_python_api import meteor_trajectory_schema


class TestMeteorTrajectorySchema(unittest.TestCase):
    """Tests for the meteor_trajectory_schema module."""

    def setUp(self) -> None:
        """
        Sets up the tests.
        """
        self.test_verbose_dataframe = pd.DataFrame(
            {
                "Trajectory (Id)": [1, 2, 3],
                "Trajectory Start Time": [1.123, 2.5423, 3.343],
                "Trajectory End Time": [2.123, 3.5423, 4.343],
                "IAU Code": ["trajectory_1", "trajectory_2", "trajectory_3"],
                "Trajectory Participating Stations": [
                    ["station_1", "station_2"],
                    ["station_3", "station_4"],
                    ["station_5", "station_6"],
                ],
            }
        )
        self.test_verbose_dataframe.set_index("Trajectory (Id)", inplace=True)

        self.test_camel_case_dataframe = pd.DataFrame(
            {
                "trajectory_id": [1, 2, 3],
                "trajectory_start_time": [1.123, 2.5423, 3.343],
                "trajectory_end_time": [2.123, 3.5423, 4.343],
                "iau_code": ["trajectory_1", "trajectory_2", "trajectory_3"],
                "trajectory_participating_stations": [
                    ["station_1", "station_2"],
                    ["station_3", "station_4"],
                    ["station_5", "station_6"],
                ],
            }
        )
        self.test_camel_case_dataframe.set_index("trajectory_id", inplace=True)

    @mock.patch("gmn_python_api.meteor_trajectory_reader.read_csv")
    def test_get_column_names(self, mock_read_csv: mock.Mock) -> None:
        """
        Test: get_column_names returns correct column names.
        When: get_column_names is called with mocked model dataframe.
        """
        mock_read_csv.return_value = self.test_verbose_dataframe

        meteor_trajectory_schema.get_column_names.cache_clear()
        self.assertEqual(
            meteor_trajectory_schema.get_column_names(),
            [
                "Trajectory (Id)",
                "Trajectory Start Time",
                "Trajectory End Time",
                "IAU Code",
                "Trajectory Participating Stations",
            ],
        )

    @mock.patch("gmn_python_api.meteor_trajectory_reader.read_csv")
    def test_get_column_names_camel_case(self, mock_read_csv: mock.Mock) -> None:
        """
        Test: get_column_names returns correct column names.
        When: get_column_names is called with mocked model dataframe and
         output_camel_case=True.
        """
        mock_read_csv.return_value = self.test_camel_case_dataframe

        meteor_trajectory_schema.get_column_names.cache_clear()
        self.assertEqual(
            meteor_trajectory_schema.get_column_names(output_camel_case=True),
            [
                "trajectory_id",
                "trajectory_start_time",
                "trajectory_end_time",
                "iau_code",
                "trajectory_participating_stations",
            ],
        )

    def test_get_model_meteor_summary_dataframe(self) -> None:
        """
        Test: get_model_meteor_summary_dataframe returns non-empty dataframe with no camelcase.
        When: get_model_meteor_summary_dataframe is called with output_camel_case=False.
        """
        meteor_trajectory_schema.get_model_meteor_trajectory_dataframe.cache_clear()
        dataframe_no_camelcase = meteor_trajectory_schema.get_model_meteor_trajectory_dataframe(
            output_camel_case=False,
        )
        self.assertFalse(dataframe_no_camelcase.empty)

    def test_get_model_meteor_summary_dataframe_camelcase(self) -> None:
        """
        Test: get_model_meteor_summary_dataframe returns non-empty dataframe with camelcase.
        When: get_model_meteor_summary_dataframe is called with output_camel_case=True.
        """
        meteor_trajectory_schema.get_model_meteor_trajectory_dataframe.cache_clear()
        dataframe_camelcase = meteor_trajectory_schema.get_model_meteor_trajectory_dataframe(
            output_camel_case=True,
        )
        self.assertFalse(dataframe_camelcase.empty)

    @mock.patch("gmn_python_api.meteor_trajectory_reader.read_csv")
    def test_get_verbose_and_camel_case_column_name_bidict(
            self, read_csv: mock.Mock
    ) -> None:
        """
        Test: get_verbose_and_camel_case_column_name_bidict produces correct dictionary.
        When: get_verbose_and_camel_case_column_name_bidict is called with mocked dataframes.
        """
        read_csv.side_effect = [
            self.test_verbose_dataframe,
            self.test_camel_case_dataframe,
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
            "Trajectory Participating Stations": "trajectory_participating_stations",
            "trajectory_participating_stations": "Trajectory Participating Stations",
        }

        meteor_trajectory_schema.get_verbose_camel_case_column_name_bidict.cache_clear()
        actual_bidict = (
            meteor_trajectory_schema.get_verbose_camel_case_column_name_bidict()
        )
        self.assertEqual(expected_bidict, actual_bidict)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
