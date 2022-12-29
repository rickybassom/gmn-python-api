# Usage

Simple meteor analysis example:

```python
from gmn_python_api import data_directory
from gmn_python_api import meteor_summary_reader as reader

# Analyse recorded meteor data for the 24th of July 2019
traj_sum_file_content = data_directory.get_daily_file_content_by_date("2019-07-24")

# Read data as a Pandas DataFrame
traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(
    traj_sum_file_content,
    csv_data_directory_format=True,
)

print(f"{traj_sum_df['Vgeo (km/s)'].max()} km/s was the fastest geostationary velocity")
# Output: 65.38499 km/s was the fastest geostationary velocity

print(f"{traj_sum_df.loc[traj_sum_df['IAU (code)'] == 'PER'].shape[0]} Perseid meteors")
# Output: 8 Perseid meteors

print(
    f"Station #{traj_sum_df['Num (stat)'].mode().values[0]} recorded the most meteors")
# Output: Station #2 recorded the most meteors
```

The trajectory summary data model can be loaded offline:

```python
from gmn_python_api import meteor_summary_reader as reader
from gmn_python_api.meteor_summary_schema import _MODEL_TRAJECTORY_SUMMARY_FILE_PATH

trajectory_summary_df = reader.read_meteor_summary_csv_as_dataframe(
    _MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
    csv_data_directory_format=True,
)
```

See the [Data Directory](data_directory.md) section for details about how to access 
trajectory summary data using
[GMN Data Directory](https://globalmeteornetwork.org/data/traj_summary_data/).

See the [REST API](rest_api.md) section for details about how to access meteor summary 
data using the
future [GMN REST API](https://github.com/gmn-data-platform/gmn-data-endpoints).

See the [Data Schemas](data_schemas.md) section for meteor/trajectory DataFrame 
features.

See the [API Reference](autoapi/gmn_python_api/index.md) section for function and 
variable definitions.
