GMN Python API
==============

|PyPI| |Status| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/gmn-python-api.svg
   :target: https://pypi.org/project/gmn-python-api/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/gmn-python-api.svg
   :target: https://pypi.org/project/gmn-python-api/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/gmn-python-api
   :target: https://pypi.org/project/gmn-python-api
   :alt: Python Version
.. |License| image:: https://img.shields.io/github/license/gmn-data-platform/gmn-python-api
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/gmn-python-api/latest.svg?label=Read%20the%20Docs
   :target: https://gmn-python-api.readthedocs.io/
   :alt: Read the documentation at https://gmn-python-api.readthedocs.io/
.. |Tests| image:: https://github.com/gmn-data-platform/gmn-python-api/workflows/Tests/badge.svg
   :target: https://github.com/gmn-data-platform/gmn-python-api/actions?query=workflow%3ATests+branch%3Amain
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/gmn-data-platform/gmn-python-api/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/gmn-data-platform/gmn-python-api
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

Python library for accessing open `Global Meteor Network`_ (GMN) meteor trajectory `data`_.
Global meteor data is generated using a network of low-light cameras pointed towards the night sky.
Meteor properties (radiants, orbits, magnitudes and masses) are produced by the GMN and are available through this library.

.. image:: https://raw.githubusercontent.com/gmn-data-platform/gmn-python-api/main/screenshot.png
  :alt: Data screenshot

|

`Demo on Google Colab`_

Features
--------

* Listing available daily and monthly csv trajectory summary files from the `GMN data directory`_.

* Downloading specific daily and monthly csv trajectory summary files from the data directory.

* Functions for loading the data directory trajectory summary data into Pandas_ DataFrames or Numpy_ arrays.

* Functions for retrieving meteor summary data from the future GMN Data Store using the GMN REST API.

* Functions for loading REST API meteor summary data into Pandas_ DataFrames or Numpy_ arrays.

* Functions for retrieving the current meteor trajectory schema in AVRO_ format.

* Functions for retrieving available IAU_ registered meteor showers.

Requirements
------------

* Python 3.7.1+, 3.8, 3.9 or 3.10


Installation
------------

You can install *GMN Python API* via pip_ from `PyPI`_:

.. code:: console

   $ pip install gmn-python-api

Or install the latest development code, through TestPyPI_ or directly from GitHub_ via pip_:

.. code:: console

   $ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple gmn-python-api==<version>
   Or
   $ pip install git+https://github.com/gmn-data-platform/gmn-python-api

There is also a `development Google Colab notebook`_.

See the Troubleshooting_ section if you encounter installation issues.

Usage
-----

Simple meteor analysis example:

.. code:: python

   from datetime import datetime
   from gmn_python_api.data_directory import get_daily_file_content_by_date
   from gmn_python_api.meteor_summary_reader import read_meteor_summary_csv_as_dataframe

   trajectory_summary_file_content = get_daily_file_content_by_date(datetime(2019, 7, 24))
   trajectory_summary_dataframe = read_meteor_summary_csv_as_dataframe(
       trajectory_summary_file_content,
       csv_data_directory_format=True,
   )

   print(f"{trajectory_summary_dataframe['Vgeo (km/s)'].max()} km/s "
          "was the fastest geostationary velocity out of all meteors for that day.")
   # 65.38499 km/s was the fastest geostationary velocity out of all meteors (24th of July 2019).

   print(f"{trajectory_summary_dataframe.loc[trajectory_summary_dataframe['IAU (code)'] == 'PER'].shape[0]} "
          "meteors were estimated to be part of the Perseids shower.")
   # 8 meteors were estimated to be part of the Perseids shower (24th of July 2019).

   print(f"Station {trajectory_summary_dataframe['Num (stat)'].mode().values[0]} "
          "recorded the highest number of meteors.")
   # Station 2 recorded the highest number of meteors (24th of July 2019).

Please see the Usage_ and `API Reference`_ section for more details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*GMN Python API* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

`Hypermodern Python Cookiecutter`_ template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/project/gmn-python-api/
.. _TestPyPI: https://test.pypi.org/project/gmn-python-api/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/gmn-data-platform/gmn-python-api/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: https://gmn-python-api.readthedocs.io/en/latest/contributing.html
.. _Usage: https://gmn-python-api.readthedocs.io/en/latest/usage.html
.. _API Reference: https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/index.html
.. _Global Meteor Network: https://globalmeteornetwork.org/
.. _data: https://globalmeteornetwork.org/data/
.. _Demo on Google Colab: https://colab.research.google.com/github/gmn-data-platform/gmn-data-endpoints/blob/dc25444cb98693081443bb31e8f6b2abbed3fde2/gmn_data_analysis_template.ipynb
.. _GMN data directory: https://globalmeteornetwork.org/data/traj_summary_data/
.. _Pandas: https://pandas.pydata.org/
.. _Numpy: https://numpy.org/
.. _GitHub: https://github.com/gmn-data-platform/gmn-python-api
.. _Troubleshooting: https://gmn-python-api.readthedocs.io/en/latest/troubleshooting.html
.. _development Google Colab notebook: https://colab.research.google.com/github/gmn-data-platform/gmn-data-endpoints/blob/main/gmn_data_analysis_template_dev.ipynb
.. _IAU: https://www.ta3.sk/IAUC22DB/MDC2007/
.. _AVRO: https://avro.apache.org/docs/current/spec.html
