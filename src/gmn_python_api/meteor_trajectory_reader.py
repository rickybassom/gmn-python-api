"""
This module contains functions to load meteor trajectory data into Pandas DataFrames.
"""
from io import StringIO
from typing import Optional, Any, Union, Dict, List
import pandas as pd  # type: ignore

from gmn_python_api.meteor_trajectory_schema import \
    get_verbose_camel_case_column_name_bidict, \
    _MODEL_METEOR_TRAJECTORY_FILE_ONE_ROW_PATH

"""The format of dates in meteor trajectory data."""
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def read_data(
        data: Union[str, List[Dict[str, Any]]],
        input_camel_case: Optional[bool] = False,
        output_camel_case: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Reads meteor trajectory data either as a CSV string or a list of dicts into a Pandas
     DataFrame. Columns available in the DataFrame can be found here:
     https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html

    :param data: The meteor trajectory data. Either a CSV string from the GMN data
     directory or a JSON from the GMN REST API.
    :param input_camel_case: If True, the input data is assumed to have camel case
        column names e.g. m_deg
    :param output_camel_case: If True, DataFrame column names will be camel cased e.g.
     m_deg

    :return: Pandas DataFrame of the meteor trajectory data.
    """
    if type(data) == list and data:
        meteor_trajectory_df = pd.DataFrame.from_records(data)

        if input_camel_case:
            meteor_trajectory_df = _convert_camel_case_to_verbose_column_names(
                meteor_trajectory_df)

    else:
        meteor_trajectory_df = pd.read_csv(
            StringIO(data, newline="\r") if data  # type: ignore
            else _MODEL_METEOR_TRAJECTORY_FILE_ONE_ROW_PATH,
            engine="python",
            sep=r"\s*;\s*",
            skiprows=[0, 5, 6],
            header=[0, 1],
            na_values=["nan", "...", "None"],
        )

        if not data:
            # Remove first example row
            meteor_trajectory_df = meteor_trajectory_df.iloc[1:]
        elif input_camel_case:
            meteor_trajectory_df = _convert_camel_case_to_verbose_column_names(
                meteor_trajectory_df)

        def extract_header(text: str) -> str:
            return " ".join(text.replace("#", "").split())

        meteor_trajectory_df.columns = meteor_trajectory_df.columns.map(
            lambda h: extract_header(h[0]) + (
                f" ({extract_header(h[1])})" if "Unnamed" not in h[1] else "")
        )

    _set_data_types(meteor_trajectory_df)

    if output_camel_case:
        _set_camel_case_column_names(meteor_trajectory_df)

    return meteor_trajectory_df


def _convert_camel_case_to_verbose_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the column names in a DataFrame containing meteor trajectory data to verbose
     e.g. beginning_utc_time to Beginning (UTC Time).

    :param dataframe: The meteor trajectory dataframe to convert the column names for.
    :return: The meteor trajectory dataframe with verbose column names.
    """
    for column in dataframe.columns:
        dataframe.rename(
            columns={column: get_verbose_camel_case_column_name_bidict()[column]},
            inplace=True)

    return dataframe


def _set_camel_case_column_names(dataframe: pd.DataFrame) -> None:
    """
    Sets the column names in a DataFrame containing meteor trajectory data to camel case
     e.g. m_deg.

    :param dataframe: The meteor trajectory dataframe to set the column names for.
    :return: None.
    """
    dataframe.columns = dataframe.columns.str.replace(
        "[^0-9a-zA-Z]+", "_", regex=True
    )
    dataframe.columns = dataframe.columns.str.rstrip("_")
    dataframe.columns = dataframe.columns.str.lstrip("_")

    # q (AU) and Q (AU) are different columns. Q (AU) is denoted with a trailing
    # underscore to avoid a name clash with q (AU).
    dataframe.columns = dataframe.columns.str.replace("Q_AU", "q_au_")

    dataframe.columns = dataframe.columns.str.lower()
    dataframe.index.name = "unique_trajectory_identifier"


def _set_data_types(dataframe: pd.DataFrame) -> None:
    """
    Sets the data types and index column in a DataFrame containing meteor trajectory
     data. The input dataframe must be in verbose column name format e.g.
     "Beginning (UTC Time)".

    :param dataframe: The meteor trajectory dataframe to set the data types for.
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
    ].apply(lambda x: x.split(","))

    dataframe.set_index("Unique trajectory (identifier)", inplace=True)
