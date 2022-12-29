# Contributor Guide

Thank you for your interest in improving this project.
This project is open-source under the [MIT license](https://opensource.org/licenses/MIT)
and welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

- [Source Code](https://github.com/gmn-data-platform/gmn-python-api)
- [Documentation](https://gmn-python-api.readthedocs.io/)
- [Issue Tracker](https://github.com/gmn-data-platform/gmn-python-api/issues)

## How to report a bug

Report bugs on the [Issue Tracker](https://github.com/gmn-data-platform/gmn-python-api/issues).

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case, and/or steps to reproduce the issue.

## How to request a feature

Request features on the [Issue Tracker](https://github.com/gmn-data-platform/gmn-python-api/issues).

## How to set up your development environment

You need Python 3.7, 3.8, 3.9, and 3.10. 
Follow this [guide](https://cookiecutter-hypermodern-python.readthedocs.io/en/2022.6.3.post1/guide.html#getting-python-mac-linux-unix) to install [pyenv](https://github.com/pyenv/pyenv) and the required Python versions.

And the following tools:

- [Poetry](https://python-poetry.org/)
- [Nox](https://nox.thea.codes/)
- [nox-poetry](https://nox-poetry.readthedocs.io/)

Install the package with development requirements:

```sh
poetry install
```

You can now run an interactive Python session, or the command-line interface:

```sh
poetry run python
```

```sh
poetry run gmn-python-api
```

## How to test the project

Run the full test suite:

```sh
nox
```

List the available Nox sessions:

```sh
nox --list-sessions
```

You can also run a specific Nox session. For example, invoke the unit test suite like this:

```sh
nox --session=tests
```

Unit tests are located in the `tests` directory, and are written using the [pytest](https://pytest.readthedocs.io/) testing framework.

## How to build the documentation

```sh
nox --session=docs
```

Built documentation is located in the `docs/_build` directory.

## How to submit changes

Open a [pull request](https://github.com/gmn-data-platform/gmn-python-api/pulls) to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:
- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains 100% code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

It is recommended to open an issue before starting work on anything. This will allow a chance to talk it over with the owners and validate your approach.

## Useful links

- https://cookiecutter-hypermodern-python.readthedocs.io/en/2021.11.26/guide.html
