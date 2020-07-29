"""Scripts for populating the db for the first time."""
from strops.operators.scripts.create.fields import create_all_fields  # noqa
from strops.operators.scripts.create.op_4fields_quark import (  # noqa
    create_dm_basis_quarks,
)
from strops.operators.scripts.create.op_4fields_nucleon import (  # noqa
    create_dm_basis_nucleons,
)
from strops.operators.scripts.create.op_4fields_nucleon_nr import (  # noqa
    create_dm_basis_nucleons_nr,
)


def create_all():
    """Creates all fields, DM-2-quark operators and DM-2-nucleon operators."""
    create_all_fields()
    create_dm_basis_quarks()
    create_dm_basis_nucleons()
    create_dm_basis_nucleons_nr()


if __name__ == "__main__":
    create_all()
