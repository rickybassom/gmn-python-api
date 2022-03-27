"""Tests for the trajectory_summary_reader.py module."""
import json
import unittest
from pathlib import Path
from typing import Any

import numpy.typing as npt
import pandas as pd  # type: ignore
from avro_validator.schema import Schema  # type: ignore
from tests.expected_gmn_trajectory_summary_reader_values import EXPECTED_COLUMN_NAMES
from tests.expected_gmn_trajectory_summary_reader_values import (
    EXPECTED_COLUMN_NAMES_CAMEL_CASE,
)
from tests.expected_gmn_trajectory_summary_reader_values import EXPECTED_DTYPES

from gmn_python_api import trajectory_summary_reader as gtsr
from gmn_python_api.trajectory_summary_schema import _MODEL_TRAJECTORY_SUMMARY_FILE_PATH
from gmn_python_api.trajectory_summary_schema import get_trajectory_summary_avro_schema


class TestGmnTrajectorySummaryReader(unittest.TestCase):
    """Tests for the trajectory_summary_reader.py module."""

    def setUp(self) -> None:
        """
        Sets up the tests.
        """
        self.test_file_path: Path = Path(_MODEL_TRAJECTORY_SUMMARY_FILE_PATH)

    def test_read_trajectory_summary_buffer_as_data_frame(self) -> None:
        """
        Test: That the trajectory summary buffer can be read as a dataframe by checking
        properties.
        When: read_trajectory_summary_buffer_as_dataframe is called.
        """
        self._test_read_trajectory_summary_using_data_frame(
            gtsr.read_trajectory_summary_as_dataframe(open(self.test_file_path).read())
        )

    def test_read_trajectory_summary_buffer_as_numpy_array(self) -> None:
        """
        Test: That the trajectory summary buffer can be read as a numpy array by
        checking properties.
        When: read_trajectory_summary_buffer_as_numpy_array is called.
        """
        self._test_read_trajectory_summary_using_numpy_array(
            gtsr.read_trajectory_summary_as_numpy_array(self.test_file_path)
        )

    def test_read_trajectory_summary_file_as_data_frame(self) -> None:
        """
        Test: That the trajectory summary file can be read as a dataframe by
        checking properties.
        When: read_trajectory_summary_file_as_dataframe is called.
        """
        self._test_read_trajectory_summary_using_data_frame(
            gtsr.read_trajectory_summary_as_dataframe(self.test_file_path)
        )

    def test_read_trajectory_summary_file_as_data_frame_camel_case(self) -> None:
        """
        Test: That the trajectory summary file can be read as a dataframe by
        checking properties with camel case column names.
        When: read_trajectory_summary_file_as_dataframe is called with camel case
        option.
        """
        actual = gtsr.read_trajectory_summary_as_dataframe(
            self.test_file_path, camel_case_column_names=True
        )
        self.assertEqual(
            actual.columns.tolist(),
            EXPECTED_COLUMN_NAMES_CAMEL_CASE,
        )

    def test_read_trajectory_summary_file_as_data_frame_avro_compatible(self) -> None:
        """
        Test: That the trajectory summary dataframe can be converted to avro format and
         abide by the schema.
        When: read_trajectory_summary_file_as_dataframe is called with avro_compatible
        option.
        """
        data_frame = gtsr.read_trajectory_summary_as_dataframe(
            self.test_file_path, avro_compatible=True
        )
        actual_rows = data_frame.to_dict(orient="records")

        schema = Schema(json.dumps(get_trajectory_summary_avro_schema()))
        parsed_schema = schema.parse()

        for row in actual_rows:
            self.assertTrue(parsed_schema.validate(row))

    def test_read_trajectory_summary_file_as_numpy_array(self) -> None:
        """
        Test: That the trajectory summary file can be read as a numpy array by checking
        properties.
        When: read_trajectory_summary_file_as_numpy_array is called.
        """
        self._test_read_trajectory_summary_using_numpy_array(
            gtsr.read_trajectory_summary_as_numpy_array(self.test_file_path)
        )

    def _test_read_trajectory_summary_using_data_frame(
        self, actual_dataframe: pd.DataFrame
    ) -> None:
        """
        Asserts properties about the dataframe.

        :param actual_dataframe: The dataframe to test.
        """
        self.assertEqual(actual_dataframe.empty, False)
        self.assertEqual(actual_dataframe.shape, (534, 86))
        self.assertEqual(
            actual_dataframe.index.tolist()[:3],
            ["20220304220741_yrPTs", "20220304221458_vpeSU", "20220304221734_ii908"],
        )
        self.assertEqual(actual_dataframe.dtypes.tolist(), EXPECTED_DTYPES)
        self.assertEqual(actual_dataframe.columns.tolist(), EXPECTED_COLUMN_NAMES)
        self.assertEqual(actual_dataframe.index.name, "Unique trajectory (identifier)")

    def _test_read_trajectory_summary_using_numpy_array(
        self, actual_numpy_array: npt.NDArray[Any]
    ) -> None:
        """
        Asserts properties about the numpy array.

        :param actual_numpy_array: The numpy array to test.
        """
        self.assertEqual(actual_numpy_array.shape, (534, 86))


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
