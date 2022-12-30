"""
This module contains functions for handling the current meteor/trajectory summary data
 schema.
"""
import os
from typing import Dict

import gmn_python_api

SCHEMA_VERSION = "1.0"
"""The supported meteor/trajectory summary data format version."""

_MODEL_TRAJECTORY_SUMMARY_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "data_models",
    "traj_summary_20220304_solrange_344.0-345.0.txt",
)
"""Model v1.0 trajectory summary file, full size."""

_MODEL_TRAJECTORY_SUMMARY_FILE_ONE_ROW_PATH = os.path.join(
    os.path.dirname(__file__),
    "data_models",
    "traj_summary_20220304_solrange_344.0-345.0_one_row.txt",
)
"""Model v1.0 trajectory summary file, just one data row."""


def get_verbose_and_camel_case_column_name_bidict() -> Dict[str, str]:
    """
    Get a bidirectional dictionary that maps the verbose and camel case column names.

    :return: A bidirectional dictionary that maps the verbose and camel case column
     names.
    """
    model = open(_MODEL_TRAJECTORY_SUMMARY_FILE_ONE_ROW_PATH, "r").read()
    bidict = {}
    df_verbose = gmn_python_api.read_meteor_summary_csv_as_dataframe(  # type: ignore
        model,
        camel_case_column_names=False,
    )
    df_camel_case = gmn_python_api.read_meteor_summary_csv_as_dataframe(  # type: ignore
        model,
        camel_case_column_names=True,
    )

    bidict[df_verbose.index.name] = df_camel_case.index.name
    bidict[df_camel_case.index.name] = df_verbose.index.name

    for col in df_verbose.columns:
        bidict[col] = df_camel_case.columns[df_verbose.columns.get_loc(col)]
        bidict[df_camel_case.columns[df_verbose.columns.get_loc(col)]] = col

    return bidict
