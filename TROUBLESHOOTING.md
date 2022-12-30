# Troubleshooting

## Numpy typing error

```bash
AttributeError: module 'numpy.typing' has no attribute 'NDArray'
```

Try installing a newer version of Numpy using:

```bash
pip install numpy>1.20.3
```

## Pandas typing error

```bash
ImportError: cannot import name 'x' from 'pandas._typing'
```

This is a known issue with some newer versions of Pandas. Try installing an older
version using:

```bash
pip uninstall pandas
pip install pandas==1.1.5
```

https://stackoverflow.com/questions/65684415/exporting-csv-shows-importerror-cannot-import-name-compressionoptions-from-p

## Scipy No BLAS/LAPACK libraries found

Install `openblas` and `lapack`, see link below.

https://github.com/scipy/scipy/issues/9005