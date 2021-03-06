"""Scripts for operator module."""
from logging import getLogger
from yaml import safe_load
from os import path
from itertools import product

from sympy import sympify

from strops.references.models import Publication
from strops.references.scripts import insert_inspirehep_entry

from strops.operators.models import FourFieldOperator
from strops.parameters.models import Parameter
from strops.schemes.models import (
    ExpansionScheme,
    ExpansionParameter,
    ExpansionOrder,
    OperatorRelation,
)


LOGGER = getLogger("strops")


INSPIREHEP_IDS = [1094068, 1353074]
SCHEME_NAME = "Nucleon-DM NRET expansion"


def get_or_create_scheme():
    """Gets or creates the expansion scheme."""
    scheme = ExpansionScheme.objects.filter(name=SCHEME_NAME).first()
    if not scheme:
        data = {
            "name": SCHEME_NAME,
            "source_scale": "nucleon",
            "target_scale": "nucleon-nr",
            "description": "Expansion non-relativistic nucleon operators into"
            " related to relativistic nucleon degrees of freedom.",
        }
        scheme = ExpansionScheme(**data).save()
        scheme.references.add(*get_or_create_references())

    return scheme


def get_or_create_references():
    """Creates scheme and operator relations as specified in [1503.04811]."""
    LOGGER.info("Looking up inspirehep ids in db %s", INSPIREHEP_IDS)
    publications = Publication.objects.filter(inspirehep_id__in=INSPIREHEP_IDS)
    if len(INSPIREHEP_IDS) != publications.count():
        for idx in set(INSPIREHEP_IDS) - set(publications):
            LOGGER.info("Extracting meta info ", idx)
            insert_inspirehep_entry(idx)
        publications = Publication.objects.filter(inspirehep_id__in=INSPIREHEP_IDS)

    return publications


def create_expansion_parameters():
    """Creates expansion parameters used in scheme (if they don't exist yet)."""
    scheme = get_or_create_scheme()
    pars = ExpansionParameter.objects.filter(scheme=scheme)
    parameters = [
        {
            "name": "momentum transfer over nucleon mass",
            "symbol": "epsilon_q",
            "description": "Momentum transfer divided by DM mass."
            " nucleon mass: q / m_N",
            "natural_size": 1 / 8,
            "scheme": scheme,
        },
        {
            "name": "v perp",
            "symbol": "epsilon_v",
            "description": "Relative DM velocity orthogonal to momentum transfer."
            " nucleon mass: v",
            "natural_size": 1.0e-3,
            "scheme": scheme,
        },
        {
            "name": "nuclear mass over DM mass",
            "symbol": "epsilon_m",
            "description": "Nuclear mass divided by DM mass.",
            "natural_size": 1.0e-2,
            "scheme": scheme,
        },
    ]
    for p in parameters:
        if not pars.filter(name=p["name"], symbol=p["symbol"]).first():
            ExpansionParameter(**p).save()


def get_or_create_parameters(parameters):
    out = []
    for data in parameters:
        par, _ = Parameter.objects.get_or_create(**data)
        out.append(par)
    return out


def _get_or_create_operator_relation(
    source_op_name=None,
    target_op_name=None,
    scheme=None,
    factor=None,
    order=None,
    references=None,
    parameters=None,
):
    source = FourFieldOperator.objects.get(name=source_op_name)
    target = FourFieldOperator.objects.get(name=target_op_name)

    relation, created = OperatorRelation.objects.get_or_create(
        source=source, target=target, scheme=scheme, factor=factor
    )
    if not created:
        return relation, created

    # Specify the order in the expansion.
    expansion_parameters = ExpansionParameter.objects.filter(scheme=scheme)
    for el in order:
        ExpansionOrder.objects.create(
            power=el["power"],
            parameter=expansion_parameters.get(symbol=el["symbol"]),
            relation=relation,
        )

    relation.references.add(*references)

    pars = get_or_create_parameters(parameters)
    unknown_symbol = sympify(relation.factor).free_symbols - set(
        par.symbol for par in pars
    )
    for symbol in unknown_symbol:
        par, _ = Parameter.objects.get_or_create(
            name=f"unknown: {scheme}, {symbol}", symbol=symbol
        )
        pars.append(par)
    relation.parameters.add(*pars)

    return relation, created


def create():
    scheme = get_or_create_scheme()
    references = get_or_create_references()
    create_expansion_parameters()

    defaults = dict(scheme=scheme, references=references)

    with open(path.abspath(__file__).replace(".py", ".yaml"), "r") as inp:
        input = safe_load(inp.read())

    for data in input:
        tmp1 = defaults.copy()
        tmp1.update(data)
        for nucleon in ["proton", "neutron"]:
            tmp2 = tmp1.copy()

            tmp2["source_op_name"] = tmp2["source_op_name"].format(nucleon=nucleon)
            tmp2["target_op_name"] = tmp2["target_op_name"].format(nucleon=nucleon)

            try:
                _get_or_create_operator_relation(**tmp2)
            except Exception as error:
                LOGGER.exception(error)
                LOGGER.error(tmp2)
