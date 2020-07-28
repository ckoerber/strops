"""Scripts for operator module."""
from itertools import product

from strops.operators.models import (
    SCALES,
    KINDS,
    CONJUGATIONS,
    Field,
    FourFieldOperator,
)


def create_all_fields():
    """Creates all allowed field combinations."""
    for scale, _ in SCALES:
        for kind, _ in KINDS[scale]:
            Field.objects.get_or_create(scale=scale, kind=kind, conjugated=False)
            if CONJUGATIONS[scale][kind]:
                Field.objects.get_or_create(scale=scale, kind=kind, conjugated=True)


LORENTZ_OPS = {
    "s": "1",
    "ps": "I*gamma_5",
    "v": "gamma_mu",
    "pv": "sigma_mu_nu",
    "t": "gamma_5*gamma_mu",
    "pt": "sigma_mu_nu*I*gamma_5",
    "tv": "sigma_mu_nu * I * delta_nu",
    "tpv": "sigma_mu_nu * I * delta_nu * I * gamma_5",
}

QUARK_PAIRS = [
    ("s", "s"),
    ("s", "ps"),
    ("ps", "s"),
    ("ps", "ps"),
    ("v", "v"),
    ("v", "pv"),
    ("pv", "v"),
    ("pv", "pv"),
]


def create_dm_basis_quarks():
    """Gets or creates all quark level dm oparators.

    Currently excludes tensors and gluon fields.
    """
    scale = "quark"
    data = {
        "field1": Field.objects.get(kind="dm", scale=scale, conjugated=True),
        "field2": Field.objects.get(kind="dm", scale=scale, conjugated=False),
    }

    for kind in ["up", "down"]:
        tmp = data.copy()
        tmp["field3"] = Field.objects.get(kind=kind, scale=scale, conjugated=True)
        tmp["field4"] = Field.objects.get(kind=kind, scale=scale, conjugated=False)

        for lk1, lk2 in product(LORENTZ_OPS.keys(), LORENTZ_OPS.keys()):
            if not (lk1, lk2) in QUARK_PAIRS:
                continue

            tmp2 = tmp.copy()
            tmp2["matrix1"] = LORENTZ_OPS[lk1]
            tmp2["matrix2"] = "1"
            tmp2["matrix3"] = LORENTZ_OPS[lk2]
            tmp2["name"] = f"{lk1}-{lk2} dm-{kind}"
            tmp2["scale"] = scale

            FourFieldOperator.objects.get_or_create(**tmp2)


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
    """Gets or creates all relativistic nucleon level dm oparators.
    """
    scale = "nucleon"
    data = {
        "field1": Field.objects.get(kind="dm", scale=scale, conjugated=True),
        "field2": Field.objects.get(kind="dm", scale=scale, conjugated=False),
    }

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
            tmp2["details"] = {"delta_nu": "q_nu/q"}

            FourFieldOperator.objects.get_or_create(**tmp2)


def main():
    """Runs all operators scripts.

    Execution order:
    1. create_all_fields
    """
    create_all_fields()
    create_dm_basis_quarks()
    create_dm_basis_nucleons()


if __name__ == "__main__":
    main()
