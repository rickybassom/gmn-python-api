Usage
=========

Simple meteor analysis example:

.. code:: python

   from datetime import datetime
   from gmn_python_api import data_directory
   from gmn_python_api import meteor_summary_reader as reader

   # Analyse recorded meteor data for the 24th of July 2019
   traj_sum_file_content = data_directory.get_daily_file_content_by_date(datetime(2019, 7, 24))

   # Read data as a Pandas DataFrame
   traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(
       traj_sum_file_content,
       csv_data_directory_format=True,
   )

   print(f"{traj_sum_df['Vgeo (km/s)'].max()} km/s was the fastest geostationary velocity")
   # Output: 65.38499 km/s was the fastest geostationary velocity

   print(f"{traj_sum_df.loc[traj_sum_df['IAU (code)'] == 'PER'].shape[0]} Perseid meteors")
   # Output: 8 Perseid meteors

   print(f"Station #{traj_sum_df['Num (stat)'].mode().values[0]} recorded the most meteors")
   # Output: Station #2 recorded the most meteors

The trajectory summary data model can be loaded offline:

.. code:: python

   from gmn_python_api import meteor_summary_reader as reader
   from gmn_python_api.meteor_summary_schema import _MODEL_TRAJECTORY_SUMMARY_FILE_PATH

   trajectory_summary_df = reader.read_meteor_summary_csv_as_dataframe(
       _MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
       csv_data_directory_format=True,
   )

See the `Data Directory`_ section for details about how to access trajectory summary data using `GMN Data Directory`_.

See the `REST API`_ section for details about how to access meteor summary data using the future `GMN REST API`_.

See the `Data Schemas`_ section for meteor/trajectory DataFrame features.

See the `API Reference`_ section for function and variable definitions.

.. _Data Directory: https://gmn-python-api.readthedocs.io/en/latest/data_directory.html
.. _GMN Data Directory: https://globalmeteornetwork.org/data/traj_summary_data/
.. _REST API: https://gmn-python-api.readthedocs.io/en/latest/rest_api.html
.. _GMN REST API: https://github.com/gmn-data-platform/gmn-data-endpoints
.. _API Reference: https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/index.html
.. _Data Schemas: https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html
