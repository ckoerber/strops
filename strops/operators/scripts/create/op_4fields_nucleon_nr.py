"""Scripts for operator module."""
from logging import getLogger

from strops.operators.models import Field, FourFieldOperator


SPIN_OPS = {
    "i": "1",
    "v": "v_i",
    "s": "sigma_i",
    "sq": "sigma_i * I * q_i",
    "vt": "epsilon_ijk * I * q_j * v_k",
    "st": "epsilon_ijk * I * sigma_j * q_k",
}

LOGGER = getLogger("strops")


OPS = {
    1: ("i", ("i",)),
    2: ("i", ("v", "v")),
    3: ("i", ("s", "vt")),
    4: ("s", ("s",)),
    5: ("s", ("vt",)),
    6: ("st", ("sq",)),
    7: ("i", ("s", "v")),
    8: ("s", ("v",)),
    9: ("s", ("st",)),
    10: ("i", ("sq",)),
    11: ("sq", ("i",)),
}


def create_dm_basis_nucleons_nr():
    """Gets or creates all relativistic nucleon level dm oparators."""
    scale = "nucleon-nr"

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

        for op_id, (dm_key, nuc_keys) in OPS.items():

            tmp2 = tmp.copy()
            tmp2["matrix1"] = SPIN_OPS[dm_key]
            tmp2["matrix2"] = "1"
            tmp2["matrix3"] = " * ".join([SPIN_OPS[nuc_key] for nuc_key in nuc_keys])
            tmp2["name"] = f"O_{op_id} dm-{kind}"
            tmp2["scale"] = scale

            try:
                _, created = FourFieldOperator.objects.get_or_create(**tmp2)
                if created:
                    n_created += 1
            except Exception as error:
                LOGGER.warning("Failed to create field for data: %s", tmp2)
                LOGGER.exception(error)

    LOGGER.info("Created %d operators", n_created)
