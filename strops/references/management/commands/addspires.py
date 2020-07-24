"""Command line script to add inspirehep.net entries to db."""
from django.core.management.base import BaseCommand
from strops.references.scripts import insert_inspirehep_entries
from logging import getLogger, DEBUG


LOGGER = getLogger("strops")


class Command(BaseCommand):
    """Command line script to add inspirehep.net entries to db."""

    help = "Add inspirehep.net entires (by id) to database."

    def add_arguments(self, parser):
        """Adds `inspires_ids` argument."""
        parser.add_argument("-i", "--inspires-ids", nargs="+", type=int)

    def handle(self, *args, **options):
        """Runs `insert_inspirehep_entries` on all provided ids."""
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            LOGGER.setLevel(DEBUG)

        LOGGER.info("Parsing inspirehep.net ids %s", options["inspires_ids"])
        n_created, errors = insert_inspirehep_entries(options["inspires_ids"])
        for error in errors:
            LOGGER.exception(error)
        LOGGER.info("Created %d new entries", n_created)
