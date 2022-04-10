"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """GMN Python API."""


if __name__ == "__main__":
    main(prog_name="gmn-python-api")  # pragma: no cover
