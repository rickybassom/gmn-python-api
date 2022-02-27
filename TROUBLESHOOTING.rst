Troubleshooting
===============

Installation
------------

**Numpy typing error**

.. code-block:: bash

    AttributeError: module 'numpy.typing' has no attribute 'NDArray'

Try installing a newer version of Numpy using:

.. code-block:: bash

   pip install numpy>1.20.3

**Pandas typing error**

.. code-block:: bash

    ImportError: cannot import name 'x' from 'pandas._typing'

This is a known issue with some newer versions of Pandas. Try installing an older version using:

.. code-block:: bash

   pip uninstall pandas
   pip install pandas==1.1.5

References:

- https://stackoverflow.com/questions/65684415/exporting-csv-shows-importerror-cannot-import-name-compressionoptions-from-p
