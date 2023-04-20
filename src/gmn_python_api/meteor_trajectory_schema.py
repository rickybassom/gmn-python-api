"""
This module contains functions for handling the current meteor trajectory data schema.
"""
import os
from pathlib import Path

import pandas as pd  # type: ignore
from typing import Dict, List
from functools import lru_cache

import gmn_python_api.meteor_trajectory_reader as meteor_trajectory_reader

SCHEMA_VERSION = "1.0"
"""The supported meteor trajectory data format version."""

_MODEL_METEOR_TRAJECTORY_FILE_PATH = Path(os.path.join(
    os.path.dirname(__file__),
    "data_models",
    "traj_summary_20220304_solrange_344.0-345.0.txt",
))
"""Model meteor trajectory file, full size."""

_MODEL_METEOR_TRAJECTORY_FILE_ONE_ROW_PATH = Path(os.path.join(
    os.path.dirname(__file__),
    "data_models",
    "traj_summary_20220304_solrange_344.0-345.0_one_row.txt",
))
"""Model meteor trajectory file, just one data row."""


@lru_cache(maxsize=None)
def get_column_names(output_camel_case: bool = False) -> List[str]:
    """
    Get the column names of the current supported meteor trajectory schema.

    :param output_camel_case: Whether to return the column names in camel case or verbose
    :return: The column names of the current supported meteor trajectory model.
    """
    dataframe = meteor_trajectory_reader.read_csv(
        _MODEL_METEOR_TRAJECTORY_FILE_ONE_ROW_PATH.read_text(),
        output_camel_case=output_camel_case
    )
    dataframe = dataframe.reset_index()
    return list(dataframe.columns.to_list())


@lru_cache(maxsize=None)
def get_model_meteor_trajectory_dataframe(output_camel_case: bool = False) -> pd.DataFrame:
    """
    Get the current supported model meteor trajectory file as a DataFrame.

    :param output_camel_case: Whether to return the column names in camel case or verbose
    :return: The model meteor trajectory file as a DataFrame.
    """
    return meteor_trajectory_reader.read_csv(
        _MODEL_METEOR_TRAJECTORY_FILE_PATH.read_text(),
        output_camel_case=output_camel_case,
    )


@lru_cache(maxsize=None)
def get_verbose_camel_case_column_name_bidict() -> Dict[str, str]:
    """
    Get a bidirectional dictionary that maps the verbose and camel case column names.

    :return: A bidirectional dictionary that maps the verbose and camel case column
     names.
    """
    model = _MODEL_METEOR_TRAJECTORY_FILE_ONE_ROW_PATH.read_text()
    bidict = {}
    df_verbose = meteor_trajectory_reader.read_csv(
        model,
        output_camel_case=False,
    )
    df_camel_case = meteor_trajectory_reader.read_csv(
        model,
        output_camel_case=True,
    )

    bidict[df_verbose.index.name] = df_camel_case.index.name
    bidict[df_camel_case.index.name] = df_verbose.index.name

    for col in df_verbose.columns:
        bidict[col] = df_camel_case.columns[df_verbose.columns.get_loc(col)]
        bidict[df_camel_case.columns[df_verbose.columns.get_loc(col)]] = col

    return bidict
