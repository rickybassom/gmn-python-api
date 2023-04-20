"""
This module contains functions to load meteor trajectory data into Pandas DataFrames.
"""
from io import StringIO
from typing import Optional
import pandas as pd  # type: ignore

from gmn_python_api.meteor_trajectory_schema import \
    get_verbose_camel_case_column_name_bidict

"""The format of dates in meteor trajectory data."""
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def read_csv(
        csv: str,
        rest_format: Optional[bool] = False,
        output_camel_case: Optional[bool] = False,
) -> pd.DataFrame:
    """
    Reads CSV meteor trajectory data from the GMN data directory or GMN REST API into a
     Pandas DataFrame. Columns available in the DataFrame can be found here:
     https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html

    :param csv: The CSV meteor trajectory data. Either from the GMN data directory or
     GMN REST API.
    :param output_camel_case: If True, column names will be camel cased e.g. m_deg
    :param rest_format: If True, the CSV headers will be treated as a GMN REST API CSV.
     If False, the CSV headers will be treated as a GMN Data Directory CSV.

    :return: Pandas DataFrame of the meteor trajectory data.
    """
    if rest_format:
        meteor_trajectory_df = pd.read_csv(
            StringIO(csv, newline="\r"), engine="python"
        )
        # Convert camel case column names to verbose names
        for column in meteor_trajectory_df.columns:
            meteor_trajectory_df.rename(
                columns={column: get_verbose_camel_case_column_name_bidict()[column]},
                inplace=True)
    else:
        meteor_trajectory_df = pd.read_csv(
            StringIO(csv, newline="\r"),
            engine="python",
            sep=r"\s*;\s*",
            skiprows=[0, 5, 6],
            header=[0, 1],
            na_values=["nan", "...", "None"],
        )

        def extract_header(text: str) -> str:
            return " ".join(text.replace("#", "").split())

        meteor_trajectory_df.columns = meteor_trajectory_df.columns.map(
            lambda h: extract_header(h[0]) + (
                f" ({extract_header(h[1])})" if "Unnamed" not in h[1] else "")
        )

    _set_data_types(meteor_trajectory_df)

    if output_camel_case and not rest_format:  # REST data is already camel cased
        _set_camel_case_column_names(meteor_trajectory_df)

    return meteor_trajectory_df


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
    ].apply(lambda x: x[1:-1].split(","))

    dataframe.set_index("Unique trajectory (identifier)", inplace=True)
