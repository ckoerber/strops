"""Command line script to initial data to the db."""
from re import compile, MULTILINE
from os import path
from logging import getLogger, DEBUG

from django.core.management.base import BaseCommand, CommandError

from strops.config.settings import ROOT_DIR
from strops.operators.models import Operator, Field
from strops.operators.scripts import run_all as run_all_op_scripts
from strops.schemes.scripts import run_all as run_all_scheme_scripts


from strops.schemes.models import ExpansionScheme, ExpansionParameter, OperatorRelation
from strops.references.scripts import insert_inspirehep_entries


LOGGER = getLogger("strops")

PAT = compile(r"\s+", MULTILINE)


class Command(BaseCommand):
    """Command line script to initial data to the db."""

    help = (
        "Add fields, operators, schemes and relations to the db."
        " Needs to start on a clean db state."
    )

    papers_file = path.join(ROOT_DIR, "strops", "references", "data", "papers.txt")
    tables = [
        Operator,
        Field,
        ExpansionScheme,
        ExpansionParameter,
        OperatorRelation,
    ]

    def add_arguments(self, parser):
        """Adds `inspires_ids` argument."""

    def handle(self, *args, **options):
        """Runs `insert_inspirehep_entries` on all provided ids."""
        verbosity = int(options["verbosity"])
        if verbosity > 1:
            LOGGER.setLevel(DEBUG)

        for table in self.tables:
            if table.objects.first():
                raise CommandError(
                    "This command should only be run on empty databases."
                    " However, the table %s contains data." % table
                )

        self.read_ids()
        run_all_op_scripts()
        run_all_scheme_scripts()

    def read_ids(self):
        """Reads inspirehep ids from papers file."""
        LOGGER.info("Reading papers into db.")
        ids = []
        with open(self.papers_file, "r") as inp:
            text = inp.read()

            text = PAT.sub(" ", text.replace(",", " "))
            ids += [idx for idx in text.split(" ") if idx]

        LOGGER.info("Parsing inspirehep.net ids %s", ids)
        n_created, errors = insert_inspirehep_entries(ids)
        for error in errors:
            LOGGER.exception(error)
        LOGGER.info("Created %d new entries", n_created)
