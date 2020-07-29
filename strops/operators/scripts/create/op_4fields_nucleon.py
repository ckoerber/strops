"""Scripts for operator module."""
from itertools import product
from logging import getLogger

from strops.operators.models import Field, FourFieldOperator
from strops.operators.scripts.create.op_4fields_quark import LORENTZ_OPS


LOGGER = getLogger("strops")

NUCLEAR_PAIRS = [
    ("s", "s"),
    ("s", "ps"),
    ("ps", "s"),
    ("ps", "ps"),
    ("v", "v"),
    ("v", "pv"),
    ("pv", "v"),
    ("pv", "pv"),
    ("v", "tv"),
    ("v", "tpv"),
    ("pv", "tv"),
    ("pv", "tpv"),
]


def create_dm_basis_nucleons():
    """Gets or creates all relativistic nucleon level dm oparators."""
    scale = "nucleon"

    LOGGER.info("Creating four-field DM operators at %s scale", scale)
    data = {
        "field1": Field.objects.get(kind="dm", scale=scale, conjugated=True),
        "field2": Field.objects.get(kind="dm", scale=scale, conjugated=False),
        "scale": scale,
    }
    LOGGER.info(
        "Operators present: %d", FourFieldOperator.objects.filter(**data).count()
    )

    n_created = 0
    for kind in ["neutron", "proton"]:
        tmp = data.copy()
        tmp["field3"] = Field.objects.get(kind=kind, scale=scale, conjugated=True)
        tmp["field4"] = Field.objects.get(kind=kind, scale=scale, conjugated=False)

        for lk1, lk2 in product(LORENTZ_OPS.keys(), LORENTZ_OPS.keys()):
            if not (lk1, lk2) in NUCLEAR_PAIRS:
                continue

            tmp2 = tmp.copy()
            tmp2["matrix1"] = LORENTZ_OPS[lk1]
            tmp2["matrix2"] = "1"
            tmp2["matrix3"] = LORENTZ_OPS[lk2]
            tmp2["name"] = f"{lk1}-{lk2} dm-{kind}"
            tmp2["scale"] = scale

            try:
                _, created = FourFieldOperator.objects.get_or_create(**tmp2)
                if created:
                    n_created += 1
            except Exception as error:
                LOGGER.warning("Failed to create field for data: %s", tmp2)
                LOGGER.exception(error)

    LOGGER.info("Created %d operators", n_created)
