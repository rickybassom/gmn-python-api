# REST API

**Still under development**

The GMN REST API provides an interface to query and retrieve meteor trajectory data  
using SQL queries. The GMN REST API is under development and is not deployed. 
The `gmn_rest_api` code is not functional yet.

## Example 1

```python
from gmn_python_api import gmn_rest_api as rest_api
from gmn_python_api import meteor_trajectory_reader

import pandas as pd

# Get first 200 rows returned using the next url
data1, next_url = rest_api.get_meteor_summary_data_reader_compatible()
data2, _ = rest_api.get_meteor_summary_data_reader_compatible(
    next_page=next_url,
)

traj_df1 = meteor_trajectory_reader.read_csv(data1, rest_format=True)
traj_df2 = meteor_trajectory_reader.read_csv(data2, rest_format=True)
traj_df = pd.concat([traj_df1, traj_df2])
```

## Example 3

```python
from gmn_python_api import gmn_rest_api as rest_api
from gmn_python_api import meteor_trajectory_reader

# Get using where_sql parameter
data, _ = rest_api.get_meteor_summary_data_reader_compatible(
    where_sql="date(beginning_utc_time)=date('2019-07-24')",
)
meteor_df = meteor_trajectory_reader.read_csv(data, rest_format=True)
```

Fields available in the Pandas Dataframes can be found in the 
[Data Schemas](./data_schemas.md) section.

More info can be found in the 
[gmn_rest_api API Reference section](autoapi/gmn_python_api/gmn_rest_api/index).
