"""
This module contains functions to load meteor/trajectory summary data into Pandas
DataFrames and numpy arrays.
"""
import math
import os.path
from io import StringIO
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional
from typing import Union

import numpy.typing as npt
import pandas as pd  # type: ignore
from pandas._typing import FilePathOrBuffer  # type: ignore

import gmn_python_api.meteor_summary_schema

"""The format of dates in meteor/trajectory summary data."""
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def read_meteor_summary_csv_as_dataframe(  # noqa: C901
    filepath_or_buffer: Union[FilePathOrBuffer, List[FilePathOrBuffer]],
    camel_case_column_names: Optional[bool] = False,
    avro_compatible: Optional[bool] = False,
    avro_long_beginning_utc_time: Optional[bool] = True,
    csv_data_directory_format: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Reads a meteor/trajectory summary file into a Pandas DataFrame.

    :param filepath_or_buffer: Path or buffer for a trajectory/meteor summary file. Or a
     list of paths or buffers (types can be mixed) that will be joined in the dataframe.
    :param camel_case_column_names: If True, column names will be camel cased e.g. m_deg
    :param avro_compatible: If True, the rows in the dataframe will match the avsc
     schema with row.to_dict().
    :param avro_long_beginning_utc_time: If True, the time column will be converted from
     a datetime object to an int64 epoch time which is compatible with the long
     timestamp-micros avro type.

    :return: Pandas DataFrame of the meteor/trajectory summary file.
    """
    if not isinstance(filepath_or_buffer, list):
        filepath_or_buffer_list = [filepath_or_buffer]
    else:
        filepath_or_buffer_list = filepath_or_buffer

    # Join list of data passed in to be used in a single dataframe
    joined_data = ""
    for item in filepath_or_buffer_list:
        if type(item) is str:
            if os.path.isfile(item):
                joined_data += open(item).read() + "\n"
            else:
                joined_data += item + "\n"
        elif isinstance(item, Path):
            joined_data += open(item).read() + "\n"
        else:
            raise TypeError(
                f"filepath_or_buffer must be of type string or bytes, or a list of those"
                f" types. Got {type(item)}."
            )

    if csv_data_directory_format:
        meteor_summary_df = pd.read_csv(
            StringIO(joined_data, newline="\r"),
            engine="python",
            sep=r"\s*;\s*",
            skiprows=[0, 5, 6],
            header=[0, 1],
            na_values=["nan", "...", "None"],
        )
        # Clean header text
        meteor_summary_df.columns = meteor_summary_df.columns.map(
            lambda h: f"{_clean_header(h[0])}{_clean_header(h[1], is_unit=True)}"
        )
    else:
        meteor_summary_df = pd.read_csv(
            StringIO(joined_data, newline="\r"), engine="python"
        )
        # Convert camel case column names to verbose names
        bidict = (
            gmn_python_api.meteor_summary_schema.get_verbose_and_camel_case_column_name_bidict()
        )
        for column in meteor_summary_df.columns:
            meteor_summary_df.rename(columns={column: bidict[column]}, inplace=True)

    # Set data types
    meteor_summary_df["Beginning (UTC Time)"] = pd.to_datetime(
        meteor_summary_df["Beginning (UTC Time)"], format=DATETIME_FORMAT
    )
    meteor_summary_df["IAU (code)"] = meteor_summary_df["IAU (code)"].astype("string")
    meteor_summary_df["IAU (No)"] = (
        meteor_summary_df["IAU (No)"].fillna(-1).astype("int64")
    )
    meteor_summary_df["Beg in (FOV)"] = meteor_summary_df["Beg in (FOV)"].map(
        {"True": True, "False": False}
    )
    meteor_summary_df["Beg in (FOV)"] = meteor_summary_df["Beg in (FOV)"].astype("bool")
    meteor_summary_df["End in (FOV)"] = meteor_summary_df["End in (FOV)"].map(
        {"True": True, "False": False}
    )
    meteor_summary_df["End in (FOV)"] = meteor_summary_df["End in (FOV)"].astype("bool")
    meteor_summary_df["Participating (stations)"] = meteor_summary_df[
        "Participating (stations)"
    ].astype("string")
    meteor_summary_df["Participating (stations)"] = meteor_summary_df[
        "Participating (stations)"
    ].apply(lambda x: x[1:-1].split(","))

    meteor_summary_df[
        "Schema (version)"
    ] = gmn_python_api.meteor_summary_schema.SCHEMA_VERSION
    meteor_summary_df["Schema (version)"] = meteor_summary_df[
        "Schema (version)"
    ].astype("string")

    meteor_summary_df.set_index("Unique trajectory (identifier)", inplace=True)

    if avro_compatible:
        camel_case_column_names = True

        if avro_long_beginning_utc_time:
            # convert datetime nano to micro epoch and round to int
            meteor_summary_df["Beginning (UTC Time)"] = (
                meteor_summary_df["Beginning (UTC Time)"].astype("int64") / 1e3
            )
            meteor_summary_df["Beginning (UTC Time)"] = (
                meteor_summary_df["Beginning (UTC Time)"].round(0).astype("int64")
            )

        meteor_summary_df["IAU (code)"] = meteor_summary_df["IAU (code)"].astype(
            "unicode"
        )
        meteor_summary_df["Schema (version)"] = meteor_summary_df[
            "Schema (version)"
        ].astype("unicode")

        # Convert null values to avro compatible types
        meteor_summary_df = meteor_summary_df.applymap(
            lambda x: None
            if x == "<NA>" or (isinstance(x, float) and math.isnan(x))
            else x
        )
        meteor_summary_df.reset_index(inplace=True)

    if camel_case_column_names:
        meteor_summary_df.columns = meteor_summary_df.columns.str.replace(
            "[^0-9a-zA-Z]+", "_", regex=True
        )
        meteor_summary_df.columns = meteor_summary_df.columns.str.rstrip("_")
        meteor_summary_df.columns = meteor_summary_df.columns.str.lstrip("_")
        meteor_summary_df.columns = meteor_summary_df.columns.str.replace(
            "Q_AU", "q_au_"
        )
        meteor_summary_df.columns = meteor_summary_df.columns.str.lower()
        meteor_summary_df.index.name = "unique_trajectory_identifier"

    return meteor_summary_df


def read_meteor_summary_csv_as_numpy_array(
    filepath_or_buffer: FilePathOrBuffer,
    camel_case_column_names: Optional[bool] = False,
    avro_compatible: Optional[bool] = False,
    avro_long_beginning_utc_time: Optional[bool] = True,
    csv_data_directory_format: Optional[bool] = False,
) -> npt.NDArray[Any]:
    """
    Reads meteor/trajectory summary data into a numpy array.

    :param filepath_or_buffer: Path or buffer for a meteor/trajectory summary file.

    :return: Numpy array of the meteor/trajectory summary file.
    """
    data_frame = read_meteor_summary_csv_as_dataframe(
        filepath_or_buffer,
        camel_case_column_names=camel_case_column_names,
        avro_compatible=avro_compatible,
        avro_long_beginning_utc_time=avro_long_beginning_utc_time,
        csv_data_directory_format=csv_data_directory_format,
    )
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
