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
""""""

_MODEL_TRAJECTORY_SUMMARY_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "data_models",
    "traj_summary_20220304_solrange_344.0-345.0.txt",
)
"""Model v2.0 trajectory summary file."""

_AVRO_PATH = os.path.join(tempfile.gettempdir(), "trajectory_summary.avro")
""""""

_AVSC_PATH = os.path.join(
    tempfile.gettempdir(), f"trajectory_summary_schema_{SCHEMA_VERSION}.avsc"
)
""""""


def get_trajectory_summary_avro_schema() -> Dict[str, Dict[str, Any]]:
    """
    Get the Avro schema (.avsc) for the current trajectory summary data format.
    :return: The Avro schema in .avsc format.
    """
    data_frame = gmn_python_api.read_trajectory_summary_as_dataframe(  # type: ignore
        _MODEL_TRAJECTORY_SUMMARY_FILE_PATH, avro_compatible=True
    )

    pdx.to_avro(_AVRO_PATH, data_frame)
    pdx.read_avro(_AVRO_PATH)

    reader = DataFileReader(open(_AVRO_PATH, "rb"), DatumReader())
    schema = json.loads(reader.meta["avro.schema"].decode())

    return dict(schema)
