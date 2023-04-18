"""
This module contains functions to load meteor/trajectory summary data into Pandas
DataFrames and NumPy arrays.
"""
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
        rest_format: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Reads trajectory summary or meteor summary REST API data directory CSV data into a
     Pandas DataFrame. Columns available in the DataFrame can be found here:
     https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html

    :param filepath_or_buffer: Path or buffer for a trajectory/meteor summary file. Or a
     list of paths or buffers (types can be mixed) that will be joined in the DataFrame.
     If using a list the first item must contain the csv header, and
     all items must either be all data directory CSVs or all REST API CSVs.
    :param camel_case_column_names: If True, column names will be camel cased e.g. m_deg
    :param rest_format: If True, the filepath_or_buffer headers will be treated as a
     REST API CSV. If False, the filepath_or_buffer headers will be treated as a CSV
     from the GMN Data Directory.

    :return: Pandas DataFrame of the meteor/trajectory summary data.
    :raises: TypeError if an invalid filepath_or_buffer type is provided.
    """
    joined_data = _join_filepath_or_buffer(filepath_or_buffer)

    if rest_format:
        meteor_summary_df = pd.read_csv(
            StringIO(joined_data, newline="\r"), engine="python"
        )
        # Convert camel case column names to verbose names
        bidict = (
            gmn_python_api.meteor_summary_schema.get_verbose_and_camel_case_column_name_bidict()
        )
        for column in meteor_summary_df.columns:
            meteor_summary_df.rename(columns={column: bidict[column]}, inplace=True)
    else:
        meteor_summary_df = pd.read_csv(
            StringIO(joined_data, newline="\r"),
            engine="python",
            sep=r"\s*;\s*",
            skiprows=[0, 5, 6],
            header=[0, 1],
            na_values=["nan", "...", "None"],
        )

        def extract_header(text: str) -> str:
            return " ".join(text.replace("#", "").split())

        meteor_summary_df.columns = meteor_summary_df.columns.map(
            lambda h: extract_header(h[0]) + (
                f" ({extract_header(h[1])})" if "Unnamed" not in h[1] else "")
        )

    _set_data_types(meteor_summary_df)

    if camel_case_column_names:
        set_camel_case_column_names(meteor_summary_df)

    return meteor_summary_df


def read_meteor_summary_csv_as_numpy_array(
        filepath_or_buffer: FilePathOrBuffer,
        camel_case_column_names: Optional[bool] = False,
        rest_format: Optional[bool] = False,
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
    :param rest_format: If True, the filepath_or_buffer headers will be treated as a
     REST API CSV. If False, the filepath_or_buffer headers will be treated as a CSV
     from the GMN Data Directory.

    :return: NumPy array of the meteor/trajectory summary data.
    :raises: TypeError if an invalid filepath_or_buffer type is provided.
    """
    data_frame = read_meteor_summary_csv_as_dataframe(
        filepath_or_buffer,
        camel_case_column_names=camel_case_column_names,
        rest_format=rest_format,
    )
    return data_frame.to_numpy()  # type: ignore


def set_camel_case_column_names(dataframe: pd.DataFrame) -> None:
    """
    Sets the column names in a dataframe containing meteor/trajectory summary data to
     camel case e.g. m_deg.

    :param dataframe: The meteor summary dataframe to set the column names for.
    :return: None.
    """
    dataframe.columns = dataframe.columns.str.replace(
        "[^0-9a-zA-Z]+", "_", regex=True
    )
    dataframe.columns = dataframe.columns.str.rstrip("_")
    dataframe.columns = dataframe.columns.str.lstrip("_")
    dataframe.columns = dataframe.columns.str.replace("Q_AU", "q_au_")
    dataframe.columns = dataframe.columns.str.lower()
    dataframe.index.name = "unique_trajectory_identifier"


def _set_data_types(dataframe: pd.DataFrame) -> None:
    """
    Sets the data types and index column in a dataframe containing raw trajectory
     summary data. The input dataframe must have the column names in verbose format e.g.
     "Beginning (UTC Time)".

    :param dataframe: The meteor summary dataframe to set the data types for.
    :return: None.
    """
    dataframe["Beginning (UTC Time)"] = pd.to_datetime(
        dataframe["Beginning (UTC Time)"], format=DATETIME_FORMAT
    )
    dataframe["IAU (code)"] = dataframe[
        "IAU (code)"].astype("string")
    dataframe["IAU (No)"] = (
        dataframe["IAU (No)"].fillna(-1).astype("int64")
    )
    dataframe["Beg in (FOV)"] = dataframe[
        "Beg in (FOV)"].map(
        {"True": True, "False": False}
    )
    dataframe["Beg in (FOV)"] = dataframe[
        "Beg in (FOV)"].astype("bool")
    dataframe["End in (FOV)"] = dataframe[
        "End in (FOV)"].map(
        {"True": True, "False": False}
    )
    dataframe["End in (FOV)"] = dataframe[
        "End in (FOV)"].astype("bool")
    dataframe["Participating (stations)"] = dataframe[
        "Participating (stations)"
    ].astype("string")
    dataframe["Participating (stations)"] = dataframe[
        "Participating (stations)"
    ].apply(lambda x: x[1:-1].split(","))
    dataframe[
        "Schema (version)"
    ] = gmn_python_api.meteor_summary_schema.SCHEMA_VERSION
    dataframe["Schema (version)"] = dataframe[
        "Schema (version)"
    ].astype("string")

    dataframe.set_index("Unique trajectory (identifier)", inplace=True)

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
