# Data Schemas

GMN data fields are accessible through Pandas DataFrames produced by the 
`gmn-python-api` library. See the 
[meteor_summary_schema API Reference section](autoapi/gmn_python_api/meteor_summary_schema/index)
for function and variable details.

## Accessing meteor trajectory summary fields code example

```python
from datetime import datetime
from gmn_python_api import data_directory
from gmn_python_api import meteor_summary_reader as reader

# Access column names (verbose)
traj_sum_file_content = data_directory.get_daily_file_content_by_date(
    datetime(2019, 7, 24))
traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(
    traj_sum_file_content,
    csv_data_directory_format=True,
    camel_case_column_names=False,
)

traj_sum_df.iloc[0]['Vgeo (km/s)']
# 63.95235

# Access column names (camel case)
traj_sum_file_content = data_directory.get_daily_file_content_by_date(
    datetime(2019, 7, 24))
traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(
    traj_sum_file_content,
    csv_data_directory_format=True,
    camel_case_column_names=True,
)

traj_sum_df.iloc[0]['vgeo_km_s']
# 63.952355
```

Verbose and camel case column names can be found below.

An [AVRO](https://avro.apache.org/docs/current/spec.html) formatted schema can be
generated using the gmn-python-api package.

## Getting the current meteor trajectory summary schema code example

```python
from gmn_python_api.meteor_summary_schema import get_meteor_summary_avro_schema

schema = get_meteor_summary_avro_schema()  # JSON dict
#  {'fields': [
#    {'name': 'unique_trajectory_identifier', 'type': ['null', 'string']},
#    {'name': 'beginning_julian_date', 'type': ['null', 'double']},
#    {'name': 'beginning_utc_time', 'type': ['null', {'logicalType': 'timestamp-micros', 'type': 'long'}]},
#    {'name': 'iau_no', 'type': ['null', 'long']},
#  ...
```

## Meteor Trajectory Features

Listing of current data schema (version 2.0).

| Verbose Name                          | Camel Case Name                  | Description                                                                                                                                       |
|---------------------------------------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Unique trajectory identifier          | Unique trajectory \(identifier\) | \(Index\) A 20\-character string containing the beginning time \(rounded to seconds\) and a truncated MD5 hash encoding the trajectory position\. |
| Beginning Julian date                 | beginning\_julian\_date          | Julian date of the beginning of the meteor\.                                                                                                      |
| Beginning \(UTC Time\)                | beginning\_utc\_time             | UTC time of the beginning of the meteor\.                                                                                                         |
| IAU \(No\)                            | iau\_no                          | IAU shower number, see https://www.ta3.sk/IAUC22DB/MDC2007/Roje/roje_lista.php. Sporadic meteors have a code -1.                                  |
| IAU \(code\)                          | iau\_code                        | Three\-letter IAU shower code\. Sporadic meteors have a code “\.\.\.”\.                                                                           |
| Sol lon \(deg\)                       | sol\_lon\_deg                    | Solar longitude of the beginning of the meteor\.                                                                                                  |
| App LST \(deg\)                       | app\_lst\_deg                    | Apparent local sidereal time of the beginning of the meteor\.                                                                                     |
| RAgeo \(deg\)                         | rageo\_deg                       | Geocentric right ascension in the J2000 epoch\.                                                                                                   |
| \+/\- \(sigma\) or \+/\- \(sigma\.x\) | sigma or sigma\_x                | One sigma error \(repeated for every previous value\)\. sigma \(without number\) is the first value\. The rest contain a number starting at 1\.   |
| DECgeo \(deg\)                        | decgeo\_deg                      | Geocentric declination in the J2000 epoch\.                                                                                                       |
| LAMgeo \(deg\)                        | lamgeo\_deg                      | Geocentric ecliptic longitude in the J2000 epoch\.                                                                                                |
| BETgeo \(deg\)                        | betgeo\_deg                      | Geocentric ecliptic latitude in the J2000 epoch\.                                                                                                 |
| Vgeo \(km/s\)                         | vgeo\_km\_s                      | Geocentric velocity\.                                                                                                                             |
| LAMhel \(deg\)                        | lamhel\_deg                      | Heliocentric ecliptic longitude in the J2000 epoch\.                                                                                              |
| BEThel \(deg\)                        | bethel\_deg                      | Heliocentric ecliptic latitude in the J2000 epoch\.                                                                                               |
| Vhel \(deg\)                          | vhel\_km\_s                      | Heliocentric velocity\.                                                                                                                           |
| a \(AU\)                              | a\_au                            | Semi\-major axis\.                                                                                                                                |
| e                                     | e                                | Eccentricity\.                                                                                                                                    |
| i \(deg\)                             | i\_deg                           | Inclination\.                                                                                                                                     |
| peri \(deg\)                          | peri\_deg                        | Argument of perihelion\.                                                                                                                          |
| node \(deg\)                          | node\_deg                        | Ascending node\.                                                                                                                                  |
| Pi \(deg\)                            | pi\_deg                          | Longitude of perihelion\.                                                                                                                         |
| b \(deg\)                             | b\_deg                           | Latitude of perihelion\.                                                                                                                          |
| q \(AU\)                              | q\_au                            | Perihelion distance\.                                                                                                                             |
| f \(deg\)                             | f\_deg                           | True anomaly at the beginning of the meteor\.                                                                                                     |
| M \(deg\)                             | m\_deg                           | Mean anomaly\.                                                                                                                                    |
| Q \(AU\)                              | q\_au\_                          | Aphelion distance\.                                                                                                                               |
| n \(deg/day\)                         | n\_deg\_day                      | Mean motion in the orbit\.                                                                                                                        |
| T                                     | t\_years                         | Orbital period\.                                                                                                                                  |
| TisserandJ                            | tisserandj                       | Tisserand's parameter with respect to Jupiter\.                                                                                                   |
| RAapp \(deg\)                         | raapp\_deg                       | Apparent ground\-fixed radiant right ascension in the epoch of date\.                                                                             |
| DECapp \(deg\)                        | decapp\_deg                      | Apparent ground\-fixed radiant declination in the epoch of date\.                                                                                 |
| Azim \+E \(of N deg\)                 | azim\_e\_of\_n\_deg              | Apparent ground\-fixed radiant azimuth \(\+east of due north convention\)\.                                                                       |
| Elev \(deg\)                          | elev\_deg                        | Apparent ground\-fixed radiant elevation \(i\.e\. entry angle\)\.                                                                                 |
| Vinit \(km/s\)                        | vinit\_km\_s                     | Apparent ground\-fixed initial velocity\.                                                                                                         |
| Vavg \(km/s\)                         | vavg\_km\_s                      | Apparent ground\-fixed average velocity\.                                                                                                         |
| LatBeg \(\+N deg\)                    | latbeg\_n\_deg                   | Latitude of the beginning of the meteor\.                                                                                                         |
| LonBeg \(\+E deg\)                    | lonbeg\_e\_deg                   | Longitude of the beginning of the meteor\.                                                                                                        |
| HtBeg \(km\)                          | htbeg\_km                        | Begin height of the meteor \(above the WGS84 ellipsoid\)\.                                                                                        |
| LatEnd \(\+N deg\)                    | latend\_n\_deg                   | Latitude of the meteor end\.                                                                                                                      |
| LonEnd \(\+E deg\)                    | lonend\_e\_deg                   | Longitude of the meteor end\.                                                                                                                     |
| HtEnd \(km\)                          | htend\_km                        | End height of the meteor \(above the WGS84 ellipsoid\)\.                                                                                          |
| Duration \(sec\)                      | duration\_sec                    | Observed meteor duration\.                                                                                                                        |
| Peak \(AbsMag\)                       | peak\_absmag                     | Peak magnitude normalized to the range of 100 km\.                                                                                                |
| Peak Ht \(km\)                        | peak\_ht\_km                     | Height at which with peak magnitude occured\.                                                                                                     |
| F \(param\)                           | f\_param                         | The F parameter defined as \(HtBeg \- PeakHt\)/\(HtBeg \- HtEnd\)                                                                                 |
| Mass kg \(tau=0\.7%\)                 | mass\_kg\_tau\_0\_7              | Mass in kilograms computed with a dimensionless luminous efficiency of 0\.7%\.                                                                    |
| Qc \(deg\)                            | qc\_deg                          | Maximum convergence angle between all stations that observed the meteor\.                                                                         |
| MedianFitErr \(arcsec\)               | medianfiterr\_arcsec             | Median angular trajectory fit errors in arc seconds\.                                                                                             |
| Beg in \(FOV\)                        | beg\_in\_fov                     | Beginning of the meteor observed by at least one camera\.                                                                                         |
| End in \(FOV\)                        | end\_in\_fov                     | Ending of the meteor observed by at least one camera\.                                                                                            |
| Num \(stat\)                          | num\_stat                        | Number of stations which observed the meteor\.                                                                                                    |
| Participating \(stations\)            | participating\_stations          | Station codes of stations which observed the meteor\.                                                                                             |
| Schema \(version\)                    | schema\_version                  | The data format version for this row\. Null values will be placed if the format does support the column\.                                         |

Source: https://globalmeteornetwork.org/data/media/GMN_orbit_data_columns.pdf