"""Table implementations related to operators."""
from itertools import chain

from django.db import models
from espressodb.base.models import Base

from sympy import Function
from sympy.physics.quantum import Dagger
from sympy.physics.quantum import Operator as SympyOperator

from strops.app.utils.fields import SympyField
from strops.app.utils.tex import latex

SCALES = [
    ("quark", "Quark"),
    ("nucleon", "Nucleon"),
    ("nucleon-nr", "Non-relativistic nuclear scale"),
]
KINDS = {
    "quark": [("up", "up"), ("down", "down"), ("strange", "strange")],
    "nucleon": [("proton", "proton"), ("neutron", "neutron"), ("pion", "pion")],
    "nucleon-nr": [("proton", "proton"), ("neutron", "neutron"), ("pion", "pion")],
}
Bar = Function("Bar")
CONJUGATIONS = {
    "quark": {"up": Bar, "down": Bar, "strange": Bar},
    "nucleon": {"proton": Bar, "neutron": Bar, "pion": None},
    "nucleon-nr": {"proton": Dagger, "neutron": Dagger, "pion": None},
}
SYMBOLS = {
    "up": "u",
    "down": "d",
    "strange": "s",
    "proton": "p",
    "neutron": "n",
    "pion": "pi",
}


class Field(Base):
    """Field representing a degree of freedom present in operators."""

    scale = models.CharField(
        max_length=256,
        choices=SCALES,
        help_text="Scale at which this degree of freedom interacts.",
    )
    kind = models.CharField(
        max_length=256,
        choices=list(chain(*list(KINDS.values()))),
        help_text="Descriptive name like"
        " 'up' for the quark scale or 'proton' for the nucleon scale.",
    )
    conjugated = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        help_text="Is field conjugated (dagger, bar) or not.",
    )

    class Meta:
        """Constraints on class."""

        unique_together = ["scale", "kind", "conjugated"]

    @property
    def symbol(self):
        """Returns symbol determined by kind."""
        return SympyOperator(SYMBOLS[self.kind])

    @property
    def expression(self):
        """Returns own expression."""
        return (
            CONJUGATIONS[self.scale][self.kind](self.symbol)
            if self.conjugated
            else self.symbol
        )

    def __str__(self):
        """Returns own name."""
        return str(self.expression)

    @property
    def latex(self):
        """Returns latex form of expression."""
        return latex(self.expression)


LORENTZ_TRAFOS = [
    ("s", "Scalar"),
    ("v", "Vector"),
    ("ps", "Pseudo Scalar"),
    ("pv", "Pseudo Vector"),
    ("t", "Tensor"),
    ("pt", "Pseudo Tensor"),
]


class Operator(Base):
    """Shared base implementation of operator classes.

    Should not be used directly.
    """

    name = models.CharField(
        max_length=256,
        help_text="Name of the operator which can be used for searches.",
        unique=True,
    )
    scale = models.CharField(
        max_length=256,
        choices=SCALES,
        help_text="Scale at which this degree of freedom interacts.",
    )
    charge = models.IntegerField(
        choices=[(1, "+"), (-1, "-")],
        help_text="Charge transformation behavior of operator.",
    )
    parity = models.IntegerField(
        choices=[(1, "+"), (-1, "-")],
        help_text="Parity transformation behavior of operator.",
    )
    time = models.IntegerField(
        choices=[(1, "+"), (-1, "-")],
        help_text="Time transformation behavior of operator.",
    )
    lorentz = models.CharField(
        choices=LORENTZ_TRAFOS,
        max_length=2,
        help_text="How does this operator behave under Lorentz transformations?",
    )
    details = models.JSONField(
        null=True,
        blank=True,
        help_text="Further optional information to specify the operator.",
    )

    @property
    def expression(self):
        """Returns own symbol
        """
        return None

    def __str__(self):
        return str(self.expression)

    @property
    def latex(self):
        """Returns latex form of expression."""
        return latex(self.expression)


class TwoFieldOperator(Operator):
    """TODO: choices for matrix field?
    """

    field1 = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        help_text="Conjugated field present on the left of the operator expression"
        " (e.g., Bar(u)).",
        related_name="operators_21",
    )
    matrix1 = SympyField(
        encoder="non-commutative-expression",
        help_text="Term representing the operator. For example $\\gamma_5$",
    )
    field2 = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        help_text="Field present on the right of the operator expression (e.g., d).",
        related_name="operators_22",
    )

    class Meta:
        unique_together = ["field1", "matrix1", "field2"]

    @property
    def expression(self):
        return self.field1.expression * self.matrix1 * self.field2.expression


# class ThreeFieldOperator(Operator):
#     field1
#     matrix1
#     field2
#     matrix2
#     field3
#
#
# class FourFieldOperator(Operator):
#     field1
#     matrix1
#     field2
#     matrix2
#     field3
