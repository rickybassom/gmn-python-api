"""Command-line interface."""
import click  # type: ignore


@click.command()  # type: ignore
@click.version_option()  # type: ignore
def main() -> None:
    """GMN Python API."""


if __name__ == "__main__":
    main(prog_name="gmn-python-api")  # pragma: no cover
