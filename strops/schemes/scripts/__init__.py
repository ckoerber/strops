"""Scripts for populating the db for the first time."""
from strops.schemes.scripts.create import create_all  # noqa


def run_all():
    """Runs all scripts.

    Order:
        create_all()
    """
    create_all()


if __name__ == "__main__":
    run_all()
