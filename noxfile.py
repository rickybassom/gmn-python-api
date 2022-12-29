"""Nox sessions."""
import os
import shutil
import sys
from pathlib import Path
from textwrap import dedent

import nox

try:
    from nox_poetry import Session
    from nox_poetry import session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None

package = "gmn_python_api"
python_versions = ["3.10", "3.9", "3.8", "3.7"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    "safety",
    "lint",
    "mypy",
    "unit-tests",
    "integration-tests",
    "docs-build",
)


@session(python="3.10")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")

    ignore_ids = [44715, 44716, 44717, 51457]  # numpy CVE-2021-41495 and CVE-2022-42969
    ignored = [f"--ignore={ignore_id}" for ignore_id in ignore_ids]
    session.run("safety", "check", "--full-report", f"--file={requirements}", *ignored)


@session(python="3.10")
def lint(session: Session) -> None:
    """Lint using flake8 and pep8-naming."""
    session.install(
        "flake8",
        "flake8-bandit",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-rst-docstrings",
        "pep8-naming",
    )
    session.run("flake8", "src", "tests")


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Static type-check using mypy."""
    args = session.posargs or ["src", "tests", "docs/conf.py"]
    session.install(".")
    session.install("mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(name="unit-tests", python=python_versions)
def unit_tests(session: Session) -> None:
    """Run the unit test suite with coverage."""
    session.install(".")
    session.install("coverage[toml]", "pytest", "pygments")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", "tests/unit",
                    *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session(name="integration-tests", python="3.10")
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    session.install(".")
    session.install("pytest")
    session.run("pytest", "tests/integration", *session.posargs)


@session
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(name="docs-build", python="3.10")
def docs_build(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    session.install(".")
    session.install("sphinx", "sphinx-click", "furo", "sphinx-autoapi", "myst-parser")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)


@session(python="3.10")
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install(".")
    session.install(
        "sphinx", "sphinx-autobuild", "sphinx-click", "furo", "sphinx-autoapi",
        "myst-parser"
    )

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-autobuild", *args)
