# GMN REST API

The GMN REST API provides an interface to query and retrieve meteor trajectory data by constructing read-only SQL queries on the [GMN Data Store](https://explore.globalmeteornetwork.org/gmn_data_store) database.

We use [Datasette](https://docs.datasette.io/en/0.64.6/json_api.html) to provide the REST API.

## HTTP GET Requests

### The General REST API Endpoint

The General REST API Endpoint allows you to make custom read-only SQL queries on the GMN Data Store. The database structure can be found [here](https://explore.globalmeteornetwork.org/gmn_data_store).

The endpoint is available at:
https://explore.globalmeteornetwork.org/gmn_rest_api?<query_parameters>

The endpoint supports the following query parameters:
- `sql`: An SQL SELECT query to execute. This is required.
- `data_shape`: The [shape](https://docs.datasette.io/en/0.64.6/json_api.html#different-shapes) of the data to return. Default is `objects`.
- `data_format`: The format of the data to return. Default is `json`. `csv` is also supported.

The structure of the response body is described [here](https://docs.datasette.io/en/0.64.6/json_api.html).

The endpoint has a maximum limit of 1000 rows. I suggest using `LIMIT` and `OFFSET` in your SQL query to paginate results.

The response will include the header "last-modified" with the last modified time of the database in nanoseconds.
You can use this when making subsequent requests to the endpoint to ensure you are using the same version of the database. E.g. when paginating results.

Queries are cached for 1 hour with a maximum size of 1GB on the server. The cache is invalidated if the GMN Data Store database has been modified by our data ingestion processes which usually run twice a day.

Queries are blocked if they take longer than 3 seconds to execute. I recommend using [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) to check the query execution plan before running a query. If you need to run a long-running query, please contact us.

### The Meteor Summary REST API Endpoint

The Meteor Summary REST API Endpoint allows you to retrieve meteor properties from the GMN Data Store in a combined format. The properties available are described [here](https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html#meteor-trajectory-features).

It does this by substituting parts of this SQL SELECT [query](https://explore.globalmeteornetwork.org/gmn_data_store/meteor_summary).

The Meteor Summary REST API endpoint is available at:
https://explore.globalmeteornetwork.org/gmn_rest_api/meteor_summary?<query_parameters>

The API supports the following query parameters:
- `where`: A SQL SELECT WHERE clause to filter the results. Default is no filter. E.g. `iau_code = 'PER'`.
- `order_by`: A SQL ORDER BY clause to order the results. Default is no order. E.g. `meteor.unique_trajectory_identifier DESC`.
- `data_shape`: The [shape](https://docs.datasette.io/en/0.64.6/json_api.html#different-shapes) of the data to return. Default is `objects`.
- `data_format`: The format of the data to return. Default is `json`. `csv` is also supported.
- `page`: The page number of the results to return. Default is 1. A maximum of 1000 results are returned per page. 0 rows are returned if the page number is greater than the number of pages of results.

The structure of the response body is described [here](https://docs.datasette.io/en/0.64.6/json_api.html).

The response will include the header "last-modified" with the last modified time of the database in nanoseconds.
You can use this when making subsequent requests to the endpoint to ensure you are using the same version of the database. E.g. when paginating results.

The response will also include the header `Link` with the `rel="next"` attribute to indicate the next page of results. E.g.
```
(</gmn_rest_api/meteor_summary?page=4&order_by=&data_format=&data_shape=&where=iau_code+%3D+%27DSA%27>; rel="next")
```
The final page of results will include no data.

Queries are cached for 1 hour with a maximum size of 1GB on the server. The cache is invalidated if the GMN Data Store database has been modified by our data ingestion processes.

Queries are blocked if they take longer than 3 seconds to execute. I recommend using [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) to check the query execution plan before running a query. If you need to run a long-running query, please contact us.

### Examples

#### Get the number of stations in the network

```sh
GET https://explore.globalmeteornetwork.org/gmn_rest_api?sql=SELECT+COUNT(*)+FROM+station
{
    "ok": true,
    "rows": [
        {
            "COUNT(*)": 348
        }
    ],
    "truncated": false
}
```


#### Get meteor properties using unique trajectory identifier

```sh
GET https://explore.globalmeteornetwork.org/gmn_rest_api/meteor_summary?where=meteor.unique_trajectory_identifier='20181225032412_2Sciw'
{
    "ok": true,
    "rows": [
        {
            "unique_trajectory_identifier": "20181225032412_2Sciw",
            "beginning_julian_date": 2458477.6418141434,
            "beginning_utc_time": "2018-12-25 03:24:12.742673",
            "iau_no": null,
            "iau_code": null,
            "sol_lon_deg": 273.012865,
            "app_lst_deg": 38.707634,
            "rageo_deg": 100.94855,
            "sigma": 0.1528,
            "decgeo_deg": 23.51387,
            "sigma_1": 0.2154,
            ...
            "participating_stations": "US0002,US0008"
        }
    ],
    "truncated": false
}
```

#### Get all recorded meteors on the 26th of December 2018 ordered by geostationary velocity

```sh
GET https://explore.globalmeteornetwork.org/gmn_rest_api/meteor_summary?where=date(beginning_utc_time)='2018-12-26'&order_by=vgeo_km_s DESC
{
    "ok": true,
    "rows": [
        {
            "unique_trajectory_identifier": "20181226073247_wguje",
            ...
        },
        {
            "unique_trajectory_identifier": "20181226090057_xsxZ2",
            ...
        },
        {
            "unique_trajectory_identifier": "20181226071615_2uV0b",
            ...
        },
        ...
    ],
    "truncated": false
}
```


## Python API

The gmn_rest_api Python module provides a Python interface to query and retrieve meteor trajectory data from the General REST API Endpoint and Meteor Summary REST API Endpoint.

Data returned from the Meteor Summary endpoint can be loaded into a [Pandas](https://pandas.pydata.org/) DataFrame using the `meteor_trajectory_reader.read_data` function:
```python
from gmn_python_api import gmn_rest_api
from gmn_python_api import meteor_trajectory_reader

data = gmn_rest_api.get_meteor_summary_data_all(where="iau_code = 'SCC' and beginning_utc_time > '2019-01-01' and beginning_utc_time < '2019-04-05'")
df = meteor_trajectory_reader.read_data(data)
#                                 Beginning (Julian date)  ... Participating (stations)
# Unique trajectory (identifier)                           ...                         
# 20190105074710_89UEE                       2.458489e+06  ...         [US0003, US0009]
# 20190127130446_CEjBA                       2.458511e+06  ...         [US0001, US0009]
# 20190128121133_bmAQL                       2.458512e+06  ...         [US0002, US0003]
# [3 rows x 85 columns]
```

See the [gmn_rest_api API Reference section](autoapi/gmn_python_api/gmn_rest_api/index) for more information.
