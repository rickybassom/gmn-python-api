"""
This module contains functions to load trajectory summary data into Pandas DataFrames
and numpy arrays.
"""
import os.path
from io import StringIO
from typing import Any

import numpy.typing as npt
import pandas as pd  # type: ignore
from pandas._typing import FilePathOrBuffer  # type: ignore

"""The format of dates in trajectory summary files."""
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

"""The trajectory schema version."""
SCHEMA_VERSION = "2.0"


def read_trajectory_summary_as_dataframe(
    filepath_or_buffer: FilePathOrBuffer, camel_case_column_names: bool = False
) -> pd.DataFrame:
    """
    Reads a trajectory summary file into a Pandas DataFrame.

    :param filepath_or_buffer: Path or buffer for a trajectory summary file.
    :param camel_case_column_names: If True, column names will be camel cased e.g. m_deg

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

    trajectory_df["Schema (version)"] = SCHEMA_VERSION
    trajectory_df["Schema (version)"] = trajectory_df["Schema (version)"].astype(
        "unicode"
    )

    trajectory_df = trajectory_df.set_index("Unique trajectory (identifier)")

    if camel_case_column_names:
        trajectory_df.columns = trajectory_df.columns.str.replace("[^0-9a-zA-Z]+", "_")
        trajectory_df.columns = trajectory_df.columns.str.rstrip("_")
        trajectory_df.columns = trajectory_df.columns.str.lstrip("_")
        trajectory_df.columns = trajectory_df.columns.str.replace("Q_AU", "q_au_")
        trajectory_df.columns = trajectory_df.columns.str.lower()

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
    # In the future use to_records() to convert to a numpy record array
    # https://github.com/pandas-dev/pandas/issues/41935
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
