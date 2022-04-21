API Usage
=========

Simple meteor analysis example:

.. code:: python

   from datetime import datetime
   from gmn_python_api.data_directory import get_daily_file_content_by_date
   from gmn_python_api.meteor_summary_reader import read_meteor_summary_csv_as_datafram

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

The trajectory summary data model can be loaded offline:

.. code:: python

   from gmn_python_api.meteor_summary_reader import read_meteor_summary_csv_as_dataframe
   from gmn_python_api.meteor_summary_schema import _MODEL_TRAJECTORY_SUMMARY_FILE_PATH

   trajectory_summary_dataframe = read_meteor_summary_csv_as_dataframe(
       _MODEL_TRAJECTORY_SUMMARY_FILE_PATH,
       csv_data_directory_format=True,
   )

See the `Data Directory`_ section for details about how to access trajectory summary data using `GMN Data Directory`_.

See the `REST API`_ section for details about how to access meteor summary data using the future `GMN REST API`_.

See the `API Reference`_ section for function and variable definitions.

See the `Data Schema`_ section for meteor/trajectory DataFrame features.

.. _Data Directory: https://gmn-python-api.readthedocs.io/en/latest/data_directory.html
.. _GMN Data Directory: https://globalmeteornetwork.org/data/traj_summary_data/
.. _REST API: https://gmn-python-api.readthedocs.io/en/latest/rest_api.html
.. _GMN REST API: https://github.com/gmn-data-platform/gmn-data-endpoints
.. _API Reference: https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/index.html
.. _Data Schema: https://gmn-python-api.readthedocs.io/en/latest/data_schema.html
