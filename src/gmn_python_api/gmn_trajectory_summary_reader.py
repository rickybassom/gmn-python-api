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

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def read_trajectory_summary_as_dataframe(
    filepath_or_buffer: FilePathOrBuffer,
) -> pd.DataFrame:
    """
    Reads a trajectory summary file into a Pandas DataFrame.
    :param filepath_or_buffer: (FilePathOrBuffer) Path or buffer for a trajectory
    summary file.
    :return: (DataFrame) Pandas DataFrame of the trajectory summary file.
    """
    if not os.path.isfile(filepath_or_buffer):
        filepath_or_buffer = StringIO(filepath_or_buffer)

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
    trajectory_df["Participating (stations)"] = trajectory_df[
        "Participating (stations)"
    ].astype("string")

    trajectory_df["Beg in (FOV)"] = trajectory_df["Beg in (FOV)"].map(
        {"True": True, "False": False}
    )
    trajectory_df["Beg in (FOV)"] = trajectory_df["Beg in (FOV)"].astype("bool")
    trajectory_df["End in (FOV)"] = trajectory_df["End in (FOV)"].map(
        {"True": True, "False": False}
    )
    trajectory_df["End in (FOV)"] = trajectory_df["End in (FOV)"].astype("bool")

    return trajectory_df


def read_trajectory_summary_as_numpy_array(
    filepath_or_buffer: FilePathOrBuffer,
) -> npt.NDArray[Any]:
    """
    Reads a trajectory summary file into a numpy array.
    :param filepath_or_buffer: (FilePathOrBuffer) Path or buffer for a trajectory
    summary file.
    :return: (ndarray) Numpy array of the trajectory summary file.
    """
    data_frame = read_trajectory_summary_as_dataframe(filepath_or_buffer)
    # In the future use to_records() to convert to a numpy record array
    # https://github.com/pandas-dev/pandas/issues/41935
    return data_frame.to_numpy()  # type: ignore


def _clean_header(text: str, is_unit: bool = False) -> str:
    """
    Extract header text from each raw csv file header.
    :param text: (str) Raw csv header
    :param is_unit: (optional bool) return text with brackets for units
    :returns: (str) Formatted text
    """
    # Return an empty string if there is no header found
    if "Unnamed" in text:
        return ""

    # Removes additional spaces and hashtags from text. Add brackets optionally.
    clean_header = " ".join(text.replace("#", "").split())
    if is_unit:
        clean_header = f" ({clean_header})"

    return clean_header
