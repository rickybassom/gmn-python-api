"""
This module contains functions to load trajectory summary data into Pandas DataFrames
and numpy arrays.
"""
import math
import os.path
from io import StringIO
from typing import Any
from typing import Optional

import numpy.typing as npt
import pandas as pd  # type: ignore
from pandas._typing import FilePathOrBuffer  # type: ignore

from gmn_python_api import trajectory_summary_schema

"""The format of dates in trajectory summary files."""
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def read_trajectory_summary_as_dataframe(
    filepath_or_buffer: FilePathOrBuffer,
    camel_case_column_names: Optional[bool] = False,
    avro_compatible: Optional[bool] = False,
    avro_long_beginning_utc_time: Optional[bool] = True,
) -> pd.DataFrame:
    """
    Reads a trajectory summary file into a Pandas DataFrame.

    :param filepath_or_buffer: Path or buffer for a trajectory summary file.
    :param camel_case_column_names: If True, column names will be camel cased e.g. m_deg
    :param avro_compatible: If True, the rows in the dataframe will match the avsc
     schema with row.to_dict().
    :param avro_long_beginning_utc_time: If True, the time column will be converted from
     a datetime object to an int64 epoch time which is compatible with the long
     timestamp-micros avro type.

    :return: Pandas DataFrame of the trajectory summary file.
    """
    if not os.path.isfile(filepath_or_buffer) and type(filepath_or_buffer) is str:
        filepath_or_buffer = StringIO(filepath_or_buffer, newline="\r")

    trajectory_df = pd.read_csv(
        filepath_or_buffer,
        engine="python",
        sep=r"\s*;\s*",
        skiprows=[0, 5, 6],
        header=[0, 1],
        na_values=["nan", "...", "None"],
    )
    # Clean header text
    trajectory_df.columns = trajectory_df.columns.map(
        lambda h: f"{_clean_header(h[0])}{_clean_header(h[1], is_unit=True)}"
    )

    # Set data types
    trajectory_df["Beginning (UTC Time)"] = pd.to_datetime(
        trajectory_df["Beginning (UTC Time)"], format=DATETIME_FORMAT
    )
    trajectory_df["IAU (code)"] = trajectory_df["IAU (code)"].astype("string")
    trajectory_df["Beg in (FOV)"] = trajectory_df["Beg in (FOV)"].map(
        {"True": True, "False": False}
    )
    trajectory_df["Beg in (FOV)"] = trajectory_df["Beg in (FOV)"].astype("bool")
    trajectory_df["End in (FOV)"] = trajectory_df["End in (FOV)"].map(
        {"True": True, "False": False}
    )
    trajectory_df["End in (FOV)"] = trajectory_df["End in (FOV)"].astype("bool")
    trajectory_df["Participating (stations)"] = trajectory_df[
        "Participating (stations)"
    ].astype("string")
    trajectory_df["Participating (stations)"] = trajectory_df[
        "Participating (stations)"
    ].apply(lambda x: x[1:-1].split(","))

    trajectory_df["Schema (version)"] = trajectory_summary_schema.SCHEMA_VERSION
    trajectory_df["Schema (version)"] = trajectory_df["Schema (version)"].astype(
        "string"
    )

    trajectory_df.set_index("Unique trajectory (identifier)", inplace=True)

    if avro_compatible:
        camel_case_column_names = True

        if avro_long_beginning_utc_time:
            # convert datetime nano to micro epoch and round to int
            trajectory_df["Beginning (UTC Time)"] = (
                trajectory_df["Beginning (UTC Time)"].astype("int64") / 1e3
            )
            trajectory_df["Beginning (UTC Time)"] = (
                trajectory_df["Beginning (UTC Time)"].round(0).astype("int64")
            )

        trajectory_df["IAU (code)"] = trajectory_df["IAU (code)"].astype("unicode")
        trajectory_df["Schema (version)"] = trajectory_df["Schema (version)"].astype(
            "unicode"
        )
        trajectory_df = trajectory_df.applymap(
            lambda x: None
            if x == "<NA>" or (isinstance(x, float) and math.isnan(x))
            else x
        )
        trajectory_df.reset_index(inplace=True)

    if camel_case_column_names:
        trajectory_df.columns = trajectory_df.columns.str.replace(
            "[^0-9a-zA-Z]+", "_", regex=True
        )
        trajectory_df.columns = trajectory_df.columns.str.rstrip("_")
        trajectory_df.columns = trajectory_df.columns.str.lstrip("_")
        trajectory_df.columns = trajectory_df.columns.str.replace("Q_AU", "q_au_")
        trajectory_df.columns = trajectory_df.columns.str.lower()
        trajectory_df.index.name = "unique_trajectory_identifier"

    return trajectory_df


def read_trajectory_summary_as_numpy_array(
    filepath_or_buffer: FilePathOrBuffer,
) -> npt.NDArray[Any]:
    """
    Reads a trajectory summary file into a numpy array.

    :param filepath_or_buffer: Path or buffer for a trajectory summary file.

    :return: Numpy array of the trajectory summary file.
    """
    data_frame = read_trajectory_summary_as_dataframe(filepath_or_buffer)
    return data_frame.to_numpy()  # type: ignore


def _clean_header(text: str, is_unit: bool = False) -> str:
    """
    Extract header text from each raw csv file header.

    :param text: Raw csv header.
    :param is_unit: return text with brackets for units.

    :returns: Formatted text.
    """
    # Return an empty string if there is no header found
    if "Unnamed" in text:
        return ""

    # Removes additional spaces and hashtags from text. Add brackets optionally.
    clean_header = " ".join(text.replace("#", "").split())
    if is_unit:
        clean_header = f" ({clean_header})"

    return clean_header
