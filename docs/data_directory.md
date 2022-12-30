# Data Directory

The GMN provides
a [Data Directory](https://globalmeteornetwork.org/data/traj_summary_data/) of
trajectory summary CSV data. The `gmn-python-api` library allows you to read from the
directory (see
[data_directory API Reference section](autoapi/gmn_python_api/data_directory/index) for 
function and variable details).

## Example 1

```python
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_summary_reader as reader

# Get meteor data from the 2019-07-24
traj_sum_file_content = dd.get_daily_file_content_by_date("2019-07-24")
traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(traj_sum_file_content)
```

## Example 2

```python
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_summary_reader as reader

# Get meteor data from the 2019-07-24 and 2019-07-25, and combine into a single dataframe
traj_sum_file_content_1 = dd.get_daily_file_content_by_date("2019-07-24")
traj_sum_file_content_2 = dd.get_daily_file_content_by_date("2019-07-25")
traj_sum_df = reader.read_meteor_summary_csv_as_dataframe([traj_sum_file_content_1, traj_sum_file_content_2])
```

## Example 3

```python
from gmn_python_api import data_directory as dd
from gmn_python_api import meteor_summary_reader as reader

# Get meteor data from July 2019
traj_sum_file_content = dd.get_monthly_file_content_by_date("2019-07")
traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(traj_sum_file_content)
```

Fields available in the Pandas Dataframes can be found in the 
[Data Schemas](./data_schemas.md) section.

More info can be found in the 
[data_directory API Reference section](autoapi/gmn_python_api/data_directory/index).
