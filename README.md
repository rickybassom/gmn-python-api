[![PyPI](https://img.shields.io/pypi/v/gmn-python-api)](https://pypi.org/project/gmn-python-api/)
[![Status](https://img.shields.io/pypi/status/gmn-python-api)](https://pypi.org/project/gmn-python-api/)
[![Python versions](https://img.shields.io/pypi/pyversions/gmn-python-api)](https://pypi.org/project/gmn-python-api/)
[![License](https://img.shields.io/pypi/l/gmn-python-api)](https://pypi.org/project/gmn-python-api/)

[![Read the Docs](https://img.shields.io/readthedocs/gmn-python-api)](https://gmn-python-api.readthedocs.io/en/latest/)
[![Tests](https://github.com/gmn-data-platform/gmn-python-api/workflows/Tests/badge.svg)](https://github.com/gmn-data-platform/gmn-python-api/actions?query=workflow%3ATests+branch%3Amain)
[![Codecov](https://codecov.io/gh/gmn-data-platform/gmn-python-api/branch/main/graph/badge.svg)](https://codecov.io/gh/gmn-data-platform/gmn-python-api)

[![Demo on Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gmn-data-platform/gmn-data-endpoints/blob/dc25444cb98693081443bb31e8f6b2abbed3fde2/gmn_data_analysis_template.ipynb)

# gmn-python-api

This library provides a Python API for accessing open 
[Global Meteor Network](https://globalmeteornetwork.org/) (GMN) meteor trajectory 
[data](https://globalmeteornetwork.org/data/). Global meteor data is generated using a 
network of low-light cameras pointed towards the night sky. Meteor properties (radiants,
orbits, magnitudes and masses) are produced by the GMN and are available through this
library.

![Screenshot of GMN data](docs/screenshot.png)

[Demo on Google Colab](https://colab.research.google.com/github/gmn-data-platform/gmn-data-endpoints/blob/dc25444cb98693081443bb31e8f6b2abbed3fde2/gmn_data_analysis_template.ipynb)

## Features

- Listing available daily and monthly csv trajectory summary files from the 
  [GMN data directory](https://globalmeteornetwork.org/data/traj_summary_data/).

- Downloading specific daily and monthly csv trajectory summary files from the data
  directory.

- Functions for loading the data directory trajectory summary data into 
  [Pandas](https://pandas.pydata.org/) DataFrames or [Numpy](https://numpy.org/) arrays.

- Functions for retrieving meteor summary data from the future GMN Data Store using the
  GMN REST API.

- Functions for loading REST API meteor summary data
  into [Pandas](https://pandas.pydata.org/) DataFrames or [Numpy](https://numpy.org/)
  arrays.

- Functions for retrieving available 
  [IAU](https://www.ta3.sk/IAUC22DB/MDC2007/Roje/roje_lista.php) registered meteor showers.

## Requirements

- Python 3.7.1+, 3.8, 3.9 or 3.10

## Installation

You can install `gmn-python-api` via [pip](https://pip.pypa.io/) from 
[PyPI](https://pypi.org/project/gmn-python-api/):

```sh
pip install gmn-python-api
```

Or install the latest development code, through 
[TestPyPI](https://test.pypi.org/project/gmn-python-api/) or directly from 
[GitHub](https://github.com/gmn-data-platform/gmn-python-api) via 
[pip](https://pip.pypa.io/):

```sh
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple gmn-python-api==<version>
```

Or

```sh
pip install git+https://github.com/gmn-data-platform/gmn-python-api
```

Refer to the [Troubleshooting] guide if you encounter any issues.

There is also a 
[development Google Colab notebook](https://colab.research.google.com/github/gmn-data-platform/gmn-data-endpoints/blob/dc25444cb98693081443bb31e8f6b2abbed3fde2/gmn_data_analysis_template.ipynb)
that can be used to install the latest development code.

## Usage

Simple meteor analysis example:

```python
from gmn_python_api import data_directory
from gmn_python_api import meteor_summary_reader as reader

# Analyse recorded meteor data for the 24th of July 2019
traj_sum_file_content = data_directory.get_daily_file_content_by_date("2019-07-24")

# Read data as a Pandas DataFrame
traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(traj_sum_file_content)

print(f"{traj_sum_df['Vgeo (km/s)'].max()} km/s was the fastest geostationary velocity")
# Output: 65.38499 km/s was the fastest geostationary velocity

print(f"{traj_sum_df.loc[traj_sum_df['IAU (code)'] == 'PER'].shape[0]} Perseid meteors")
# Output: 8 Perseid meteors

print(f"Station #{traj_sum_df['Num (stat)'].mode().values[0]} recorded the most meteors")
# Output: Station #2 recorded the most meteors
```

Please see the [Usage](https://gmn-python-api.readthedocs.io/en/latest/usage.html) and 
[API Reference](https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/index.html)
sections for more details.

## Contributing
Contributions are very welcome. To learn more, see the 
[Contributing guide].

## License

Distributed under the terms of the [MIT](https://opensource.org/licenses/MIT) license,
`gmn-python-api` is free and open source software.

<!-- Links -->
[Troubleshooting]: ./TROUBLESHOOTING.md
[Contributing guide]: ./CONTRIBUTING.md
