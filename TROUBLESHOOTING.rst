Troubleshooting
===============

Installation
------------

**Pandas Typing Error**

.. code-block:: bash

    ImportError: cannot import name 'x' from 'pandas._typing'

This is a known issue with some newer versions of Pandas. Try installing an older version using:

.. code-block:: bash

   pip uninstall pandas
   pip install pandas==1.1.5

References:

- https://stackoverflow.com/questions/65684415/exporting-csv-shows-importerror-cannot-import-name-compressionoptions-from-p
