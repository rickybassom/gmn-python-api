"""
This module contains functions for handling the current trajectory summary data schema.
"""
import json
import os
import tempfile
from typing import Any
from typing import Dict

import pandavro as pdx  # type: ignore
from avro.datafile import DataFileReader  # type: ignore
from avro.io import DatumReader  # type: ignore

import gmn_python_api


SCHEMA_VERSION = "2.0"
"""The supported trajectory summary data format version."""

_MODEL_TRAJECTORY_SUMMARY_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "data_models",
    "traj_summary_20220304_solrange_344.0-345.0.txt",
)
"""Model v2.0 trajectory summary file."""

_AVSC_PATH = os.path.join(
    tempfile.gettempdir(), f"trajectory_summary_schema_{SCHEMA_VERSION}.avsc"
)
"""The path for the temporary Avro schema file that will be returned as a string."""


def get_trajectory_summary_avro_schema() -> Dict[str, Dict[str, Any]]:
    """
    Get the Avro schema (.avsc) for the current trajectory summary data format.
    :return: The Avro schema in .avsc format.
    """
    _, avro_file_path = tempfile.mkstemp()

    data_frame = gmn_python_api.read_trajectory_summary_as_dataframe(  # type: ignore
        _MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
        avro_compatible=True,
        avro_long_beginning_utc_time=False,
    )

    pdx.to_avro(avro_file_path, data_frame)
    pdx.read_avro(avro_file_path)

    reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
    schema = json.loads(reader.meta["avro.schema"].decode())

    return dict(schema)
