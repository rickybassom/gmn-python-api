Data Directory
==============

The GMN provides a `Data Directory`_ of trajectory summary CSV data. The gmn-python-api library allows you to read from the directory (see `data_directory API reference section`_ for function and variable details).


Example 1:

.. code:: python

   from datetime import datetime
   from gmn_python_api import data_directory
   from gmn_python_api import meteor_summary_reader as reader

   # Get meteor data from the 24/7/2019
   traj_sum_file_content = data_directory.get_daily_file_content_by_date(datetime(2019, 7, 24))
   traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(
       traj_sum_file_content,
       csv_data_directory_format=True,
   )

Example 2:

.. code:: python

   from datetime import datetime
   from gmn_python_api import data_directory
   from gmn_python_api import meteor_summary_reader as reader

   # Get meteor data from the 24/7/2019 and 25/7/2019, and combine into a single dataframe
   traj_sum_file_content_1 = data_directory.get_daily_file_content_by_date(datetime(2019, 7, 24))
   traj_sum_file_content_2 = data_directory.get_daily_file_content_by_date(datetime(2019, 7, 25))
   traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(
       [traj_sum_file_content_1, traj_sum_file_content_2],
       csv_data_directory_format=True,
   )

Example 3:

.. code:: python

   from datetime import datetime
   from gmn_python_api import data_directory
   from gmn_python_api import meteor_summary_reader as reader

   # Get meteor data from July 2019
   traj_sum_file_content = data_directory.get_monthly_file_content_by_date(datetime(2019, 7, 1))
   traj_sum_df = reader.read_meteor_summary_csv_as_dataframe(
       traj_sum_file_content,
       csv_data_directory_format=True,
   )


Fields available in the Pandas Dataframes can be found in the `Data Schemas`_ section.

More info can be found in the `data_directory API Reference section`_.

.. _data_directory API Reference section: https://gmn-python-api.readthedocs.io/en/latest/autoapi/gmn_python_api/data_directory/index.html
.. _Data Directory: https://globalmeteornetwork.org/data/traj_summary_data/
.. _Data Schemas: https://gmn-python-api.readthedocs.io/en/latest/data_schemas.html
