# REST API

The [GMN REST API](https://github.com/gmn-data-platform/gmn-rest-api) provides an
interface to query and retrieve data from the GMN Data Store. The GMN REST API and
the [GMN Data Store](https://github.com/gmn-data-platform/gmn-data-store) are not yet
deployed on the GMN server, but they can be deployed locally (see 
[development data analysis notebook](https://colab.research.google.com/github/gmn-data-platform/gmn-data-endpoints/blob/cef0b3721737e8d65002d21dc56aa27d74003593/gmn_data_analysis_template_dev.ipynb))
.

[Datasette](https://datasette.io/) is used for the REST API and provides endpoints to
select data from the readonly GMN Data Store database using SQL. See the 
[gmn_rest_api API Reference section](autoapi/gmn_python_api/gmn_rest_api/index) for 
function and variable details. Note that data returned from the API is paginated, the 
function doc strings describe how to fetch the next page of data.

## Example 1

```python
from gmn_python_api import gmn_rest_api as rest_api
from gmn_python_api import meteor_summary_reader as reader

# Get first 200 rows returned using the next url
data1, next_url = rest_api.get_meteor_summary_data_reader_compatible()
data2, _ = rest_api.get_meteor_summary_data_reader_compatible(
    next_page=next_url,
)
meteor_df = reader.read_meteor_summary_csv_as_dataframe([data1, data2])
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
meteor_df = reader.read_meteor_summary_csv_as_dataframe([data1, data2])
```

## Example 3

```python
from gmn_python_api import gmn_rest_api as rest_api
from gmn_python_api import meteor_summary_reader as reader

# Get using where_sql parameter
data, _ = rest_api.get_meteor_summary_data_reader_compatible(
    where_sql="date(beginning_utc_time)=date('2019-07-24')",
)
meteor_df = reader.read_meteor_summary_csv_as_dataframe(data)
```

Fields available in the Pandas Dataframes can be found in the 
[Data Schemas](./data_schemas.md) section.

More info can be found in the 
[gmn_rest_api API Reference section](autoapi/gmn_python_api/gmn_rest_api/index).
