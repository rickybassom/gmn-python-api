# Usage

Simple meteor analysis example:

```python
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_trajectory_reader

# Analyse recorded meteor data for the 24th of July 2019
traj_file_content = dd.get_daily_file_content_by_date("2019-07-24")

# Read data as a Pandas DataFrame
traj_df = meteor_trajectory_reader.read_data(traj_file_content)

print(f"{traj_df['Vgeo (km/s)'].max()} km/s was the fastest geostationary velocity")
# Output: 65.38499 km/s was the fastest geostationary velocity

print(f"{traj_df.loc[traj_df['IAU (code)'] == 'PER'].shape[0]} Perseid meteors")
# Output: 3 Perseid meteors

print(f"Station #{traj_df['Num (stat)'].mode().values[0]} recorded the most meteors")
# Output: Station #2 recorded the most meteors
```

The meteor trajectory data model can be loaded offline:

```python
from gmn_python_api.meteor_trajectory_schema import get_model_meteor_trajectory_dataframe

traj_df = get_model_meteor_trajectory_dataframe()
```

See the [Data Directory](data_directory.md) section for details about how to access 
meteor trajectory data using the 
[GMN Data Directory](https://globalmeteornetwork.org/data/traj_summary_data/).

See the [REST API](rest_api.md) section for details about how to access meteor
trajectory data using the GMN REST API.

See the [Data Schemas](data_schemas.md) section for meteor trajectory DataFrame 
features.

See the [API Reference](autoapi/gmn_python_api/index) section for function and 
variable definitions.
