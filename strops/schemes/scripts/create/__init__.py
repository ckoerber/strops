"""Scripts for populating the db for the first time."""
from strops.schemes.scripts.create import arxiv_150304811_q2n  # noqa
from strops.schemes.scripts.create import arxiv_150304811_q2nr  # noqa


def create_all():
    """Creates all fields, DM-2-quark operators and DM-2-nucleon operators."""
    arxiv_150304811_q2n.create()
    arxiv_150304811_q2nr.create()


if __name__ == "__main__":
    create_all()
