"""Command line script to add inspirehep.net entries to db."""
from re import compile, MULTILINE
from django.core.management.base import BaseCommand
from strops.references.scripts import insert_inspirehep_entries
from logging import getLogger, DEBUG


LOGGER = getLogger("strops")

PAT = compile(r"\s+", MULTILINE)


class Command(BaseCommand):
    """Command line script to add inspirehep.net entries to db."""

    help = "Add inspirehep.net entires (by id) to database."

    def add_arguments(self, parser):
        """Adds `inspires_ids` argument."""
        parser.add_argument("-i", "--inspires-ids", nargs="+", type=int)
        parser.add_argument("-r", "--read-file", type=str, help="Read ids from file.")

    def handle(self, *args, **options):
        """Runs `insert_inspirehep_entries` on all provided ids."""
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            LOGGER.setLevel(DEBUG)

        ids = []
        if options["read_file"]:
            with open(options["read_file"], "r") as inp:
                text = inp.read()

            text = PAT.sub(" ", text.replace(",", " "))
            ids += [idx for idx in text.split(" ") if idx]

        if options["inspires_ids"]:
            ids += options["inspires_ids"]

        LOGGER.info("Parsing inspirehep.net ids %s", ids)
        n_created, errors = insert_inspirehep_entries(ids)
        for error in errors:
            LOGGER.exception(error)
        LOGGER.info("Created %d new entries", n_created)
