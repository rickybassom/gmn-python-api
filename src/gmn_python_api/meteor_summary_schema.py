"""
This module contains functions for handling the current meteor/trajectory summary data
 schema.
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
"""The supported meteor/trajectory summary data format version."""

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


def get_meteor_summary_avro_schema() -> Dict[str, Dict[str, Any]]:
    """
    Get the Avro schema (.avsc) for the current meteor/trajectory summary data format.

    :return: The Avro schema in .avsc format.
    """
    _, avro_file_path = tempfile.mkstemp()

    data_frame = gmn_python_api.read_meteor_summary_csv_as_dataframe(  # type: ignore
        _MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
        avro_compatible=True,
        avro_long_beginning_utc_time=False,
        csv_data_directory_format=True,
    )

    pdx.to_avro(avro_file_path, data_frame)
    pdx.read_avro(avro_file_path)

    reader = DataFileReader(open(avro_file_path, "rb"), DatumReader())
    schema = json.loads(reader.meta["avro.schema"].decode())

    return dict(schema)


def get_verbose_and_camel_case_column_name_bidict() -> Dict[str, str]:
    """
    Get a bidirectional dictionary that maps the verbose and camel case column names.

    :return: A bidirectional dictionary that maps the verbose and camel case column
     names.
    """
    bidict = {}
    df_verbose = gmn_python_api.read_meteor_summary_csv_as_dataframe(  # type: ignore
        _MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
        camel_case_column_names=False,
        csv_data_directory_format=True,
    )
    df_camel_case = gmn_python_api.read_meteor_summary_csv_as_dataframe(  # type: ignore
        _MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
        camel_case_column_names=True,
        csv_data_directory_format=True,
    )

    bidict[df_verbose.index.name] = df_camel_case.index.name
    bidict[df_camel_case.index.name] = df_verbose.index.name

    for col in df_verbose.columns:
        bidict[col] = df_camel_case.columns[df_verbose.columns.get_loc(col)]
        bidict[df_camel_case.columns[df_verbose.columns.get_loc(col)]] = col

    return bidict
