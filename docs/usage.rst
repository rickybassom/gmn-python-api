API Usage
=========

Simple API example:

.. code:: python

   from datetime import datetime
   from gmn_python_api.data_directory import get_daily_file_content_by_date
   from gmn_python_api.trajectory_summary_reader import read_trajectory_summary_as_dataframe

   # Load the contents of a specific daily trajectory summary file into a Pandas DataFrame
   trajectory_summary_file_content = get_daily_file_content_by_date(datetime(2019, 7, 24))
   trajectory_summary_dataframe = read_trajectory_summary_as_dataframe(trajectory_summary_file_content)

   print("For the 24th of July 2019, the following data was recorded by the GMN:")
   print(f"- {trajectory_summary_dataframe['Vgeo (km/s)'].max()} km/s was the fastest geostationary velocity out of all meteors for that day.")
   print(f"- {trajectory_summary_dataframe.loc[trajectory_summary_dataframe['IAU (code)'] == 'PER'].shape[0]} meteors were estimated to be part of the Perseids shower.")
   print(f"- Station #{trajectory_summary_dataframe['Num (stat)'].mode().values[0]} recorded the highest number of meteors.")

   # Output:
   # For the 24th of July 2019, the following data was recorded by the GMN:
   # - 65.38499 km/s was the fastest geostationary velocity out of all meteors for that day.
   # - 8 meteors were estimated to be part of the Perseids shower.
   # - Station #2 recorded the highest number of meteors.

TODO: Add more examples.

Please see the API_ section for more details.

Command Line Interface
======================

TODO: CLI and section

.. click:: gmn_python_api.__main__:main
   :prog: gmn-python-api
   :nested: full

.. _API: https://gmn-python-api.readthedocs.io/en/latest/gmn_python_api/gmn_python_api/index.html
