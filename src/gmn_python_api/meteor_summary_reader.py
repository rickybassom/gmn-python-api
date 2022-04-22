"""
This module contains functions to load meteor/trajectory summary data into Pandas
DataFrames and NumPy arrays.
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


def read_meteor_summary_csv_as_dataframe(
    filepath_or_buffer: Union[FilePathOrBuffer, List[FilePathOrBuffer]],
    camel_case_column_names: Optional[bool] = False,
    avro_compatible: Optional[bool] = False,
    avro_long_beginning_utc_time: Optional[bool] = True,
    csv_data_directory_format: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Reads meteor summary REST API or trajectory summary data directory CSV data into a
     Pandas DataFrame. Columns available in the DataFrame can be found here:
     https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html

    :param filepath_or_buffer: Path or buffer for a trajectory/meteor summary file. Or a
     list of paths or buffers (types can be mixed) that will be joined in the DataFrame.
     If using a list the first item must contain the csv header, and
     all items must either be all data directory CSVs or all REST API CSVs.
    :param camel_case_column_names: If True, column names will be camel cased e.g. m_deg
    :param avro_compatible: If True, the types and column names in the DataFrame will
     match exactly the AVSC schema with row.to_dict(). AVRO AVSC Schema can be found
     with the get_meteor_summary_avro_schema function.
    :param avro_long_beginning_utc_time: If True, the time column will be converted from
     a datetime object to an int64 epoch time which is compatible with the long
     timestamp-micros avro type.
    :param csv_data_directory_format: If True, the filepath_or_buffer headers will be
     treated as a CSV from the GMN Data Directory. If False, the filepath_or_buffer
     headers will be treated as a REST API CSV.

    :return: Pandas DataFrame of the meteor/trajectory summary data.
    :raises: TypeError if an invalid filepath_or_buffer type is provided.
    """
    joined_data = _join_filepath_or_buffer(filepath_or_buffer)

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
    Reads meteor summary REST API or trajectory summary data directory CSV data into a
     NumPy array. Similar to read_meteor_summary_csv_as_dataframe. Columns available in
     the DataFrame can be found here:
     https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html

    :param filepath_or_buffer: Path or buffer for a trajectory/meteor summary file. Or a
     list of paths or buffers (types can be mixed) that will be joined in the array.
     If using a list the first item must contain the csv header, and
     all items must either be all Data Directory CSVs or all REST API CSVs.
    :param camel_case_column_names: If True, column names will be camel cased e.g. m_deg
    :param avro_compatible: If True, the types and column names in the array will
     match exactly the AVSC schema with row.to_dict(). AVRO AVSC Schema can be found
     with the get_meteor_summary_avro_schema function.
    :param avro_long_beginning_utc_time: If True, the time column will be converted from
     a datetime object to an int64 epoch time which is compatible with the long
     timestamp-micros avro type.
    :param csv_data_directory_format: If True, the filepath_or_buffer headers will be
     treated as a CSV from the GMN Data Directory. If False, the filepath_or_buffer
     headers will be treated as a REST API CSV.

    :return: NumPy array of the meteor/trajectory summary data.
    :raises: TypeError if an invalid filepath_or_buffer type is provided.
    """
    data_frame = read_meteor_summary_csv_as_dataframe(
        filepath_or_buffer,
        camel_case_column_names=camel_case_column_names,
        avro_compatible=avro_compatible,
        avro_long_beginning_utc_time=avro_long_beginning_utc_time,
        csv_data_directory_format=csv_data_directory_format,
    )
    return data_frame.to_numpy()  # type: ignore


def _join_filepath_or_buffer(  # noqa: C901
    filepath_or_buffer: Union[FilePathOrBuffer, List[FilePathOrBuffer]]
) -> str:
    """
    Join data provided in the reader filepath_or_buffer parameter into a single CSV
     string that can be read by the reader function.

    :param filepath_or_buffer: Path or buffer for a trajectory/meteor summary file. Or a
     list of paths or buffers (types can be mixed) that will be joined in the dataframe.
     If using a list the first item must contain the csv header, and
     all items must either be all data directory CSVs or all REST API CSVs.
    :param csv_data_directory_format: If True, the filepath_or_buffer headers will be
     treated as a CSV from the GMN Data Directory. If False, the filepath_or_buffer
     headers will be treated as a REST API CSV.

    :return: The joined CSV data.
    :raises: TypeError if an invalid filepath_or_buffer type is provided.
    """
    if not isinstance(filepath_or_buffer, list):
        filepath_or_buffer_list = [filepath_or_buffer]
    else:
        filepath_or_buffer_list = filepath_or_buffer

    # Join list of data passed in to a single CSV
    joined_data = ""
    for i, item in enumerate(filepath_or_buffer_list):
        if type(item) is str:
            if os.path.isfile(item):
                new_data = open(item).read() + "\n"
            else:
                new_data = item + "\n"
        elif isinstance(item, Path):
            new_data = open(item).read() + "\n"
        else:
            raise TypeError(
                f"filepath_or_buffer must be of type string or bytes, or a list of those"
                f" types. Got {type(item)}."
            )

        # Remove multiple headers in data by only keeping the first header
        if i > 0:
            new_data_lines = new_data.split("\n")

            # For REST API CSV header
            if new_data_lines[0].startswith("unique_trajectory_identifier,"):
                new_data_lines = new_data_lines[1:]

            # For data directory CSV header
            # Splice out lines that start with a #, break after # stops
            elif new_data_lines[0][0] == "#":
                for j, line in enumerate(new_data_lines):  # pragma: no branch
                    line = line.replace("\n", "").replace("\r", "")
                    if line != "" and line[0] != "#":
                        new_data_lines = new_data_lines[j:]
                        break

            new_data = "\n".join(new_data_lines)

        joined_data += new_data
        i += 1

    return joined_data


def _clean_header(text: str, is_unit: bool = False) -> str:
    """
    Extract header text from each raw trajectory summary csv file header.

    :param text: Raw trajectory summary csv column header text.
    :param is_unit: If True, return text with brackets for units.

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
