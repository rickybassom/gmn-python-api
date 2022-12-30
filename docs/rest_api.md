# REST API

**Still under development**

The GMN REST API provides an interface to query and retrieve data from the GMN Data 
Store with more precision. The GMN REST API is under development and is not deployed. 
The `gmn_rest_api` code is not functional yet.

## Example 1

```python
from gmn_python_api import gmn_rest_api as rest_api
from gmn_python_api import meteor_summary_reader as reader

# Get first 200 rows returned using the next url
data1, next_url = rest_api.get_meteor_summary_data_reader_compatible()
data2, _ = rest_api.get_meteor_summary_data_reader_compatible(
    next_page=next_url,
)
meteor_df = reader.read_meteor_summary_csv_as_dataframe([data1, data2], rest_format=True)
```

## Example 2

```python
from gmn_python_api import gmn_rest_api as rest_api
from gmn_python_api import meteor_summary_reader as reader

# Get first 200 rows returned using the next url
data1, next_url = rest_api.get_meteor_summary_data_reader_compatible()
data2, _ = rest_api.get_meteor_summary_data_reader_compatible(
    next_page=next_url,
)
meteor_df = reader.read_meteor_summary_csv_as_dataframe([data1, data2], rest_format=True)
```

## Example 3

```python
from gmn_python_api import gmn_rest_api as rest_api
from gmn_python_api import meteor_summary_reader as reader

# Get using where_sql parameter
data, _ = rest_api.get_meteor_summary_data_reader_compatible(
    where_sql="date(beginning_utc_time)=date('2019-07-24')",
)
meteor_df = reader.read_meteor_summary_csv_as_dataframe(data, rest_format=True)
```

Fields available in the Pandas Dataframes can be found in the 
[Data Schemas](./data_schemas.md) section.

More info can be found in the 
[gmn_rest_api API Reference section](autoapi/gmn_python_api/gmn_rest_api/index).
