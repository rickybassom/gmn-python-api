Data Directory
==============

The GMN provides a `Data Directory`_ of trajectory summary CSV data. The gmn-python-api package allows you to read from the directory (see `data_directory API reference section`_ for function and variable details).


Example 1:

.. code:: python

   from datetime import datetime
   from gmn_python_api.data_directory import get_daily_file_content_by_date
   from gmn_python_api.meteor_summary_reader import read_meteor_summary_csv_as_dataframe

   # Get meteor data from the 24/7/2019

   trajectory_summary_file_content = get_daily_file_content_by_date(datetime(2019, 7, 24))
   trajectory_summary_dataframe = read_meteor_summary_csv_as_dataframe(
       trajectory_summary_file_content,
       csv_data_directory_format=True,
   )

Example 2:

.. code:: python

   from datetime import datetime
   from gmn_python_api.data_directory import get_daily_file_content_by_date
   from gmn_python_api.meteor_summary_reader import read_meteor_summary_csv_as_dataframe

   # Get meteor data from the 24/7/2019 and 25/7/2019, and combine into a single dataframe.

   trajectory_summary_file_content_1 = get_daily_file_content_by_date(datetime(2019, 7, 24))
   trajectory_summary_file_content_2 = get_daily_file_content_by_date(datetime(2019, 7, 25))
   trajectory_summary_dataframe = read_meteor_summary_csv_as_dataframe(
       [trajectory_summary_file_content_1, trajectory_summary_file_content_2],
       csv_data_directory_format=True,
   )

Example 3:

.. code:: python

   from datetime import datetime
   from gmn_python_api.data_directory import get_monthly_file_content_by_date
   from gmn_python_api.meteor_summary_reader import read_meteor_summary_csv_as_dataframe

   # Get meteor data from July 2019

   trajectory_summary_file_content = get_monthly_file_content_by_date(datetime(2019, 7, 1))
   trajectory_summary_dataframe = read_meteor_summary_csv_as_dataframe(
       trajectory_summary_file_content,
       csv_data_directory_format=True,
   )


Fields available in the Pandas Dataframes can be found in the `Data Schemas`_ section.

More info can be found in the `data_directory API reference section`_.

.. _data_directory API reference section: https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/data_directory/index.html
.. _Data Directory: https://globalmeteornetwork.org/data/traj_summary_data/
.. _Data Schemas: https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html
