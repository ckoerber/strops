"""Scripts for populating the db for the first time."""
from strops.schemes.scripts.create import arxiv_150304811  # noqa


def create_all():
    """Creates all fields, DM-2-quark operators and DM-2-nucleon operators."""
    arxiv_150304811.create()


if __name__ == "__main__":
    create_all()
