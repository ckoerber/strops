"""Table implementations related to operators."""
from itertools import chain

from django.urls import reverse
from django.db import models
from espressodb.base.models import Base

from sympy import Function
from sympy.physics.quantum import Dagger
from sympy.physics.quantum import Operator as SympyOperator

from strops.utils.fields import SympyField
from strops.utils.tex import latex

# For html redirects, it is assumed that the first el of scales has no underscore!
SCALES = [
    ("quark", "Quark"),
    ("nucleon", "Nucleon"),
    ("nucleon-nr", "Non-relativistic nuclear scale"),
]
KINDS = {
    "quark": [
        ("up", "up"),
        ("down", "down"),
        ("strange", "strange"),
        ("dm", "Dark Matter"),
    ],
    "nucleon": [
        ("proton", "proton"),
        ("neutron", "neutron"),
        ("pion", "pion"),
        ("dm", "Dark Matter"),
    ],
    "nucleon-nr": [
        ("proton", "proton"),
        ("neutron", "neutron"),
        ("pion", "pion"),
        ("dm", "Dark Matter"),
    ],
}
Bar = Function("Bar")
CONJUGATIONS = {
    "quark": {"up": Bar, "down": Bar, "strange": Bar, "dm": Bar},
    "nucleon": {"proton": Bar, "neutron": Bar, "pion": None, "dm": Bar},
    "nucleon-nr": {"proton": Dagger, "neutron": Dagger, "pion": None, "dm": Dagger},
}
SYMBOLS = {
    "up": "u",
    "down": "d",
    "strange": "s",
    "proton": "p",
    "neutron": "n",
    "pion": "pi",
    "dm": "chi",
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
        return f"{self.expression} @ {self.scale}"

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
    details = models.JSONField(
        null=True,
        blank=True,
        help_text="Further optional information to specify the operator.",
    )

    @property
    def expression(self):
        """Returns own symbol."""
        if self.specialization != self:
            return self.specialization.expression
        return None

    def __str__(self):
        """Returns string of expression."""
        return str(self.expression)

    @property
    def latex(self):
        """Returns latex form of expression."""
        return latex(self.expression)

    def get_absolute_url(self):
        return reverse("operators:operator-detail", args=[str(self.id)])


class TwoFieldOperator(Operator):
    """Bilinear field operator table.

    TODO: choices for matrix field?
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
        """Implments unique constraint."""

        unique_together = ["field1", "matrix1", "field2"]

    def check_consistency(self):
        """Checks operator properties.

        Tests in order:
        1. Fields are specified at the same scale
        2. Own scale is equal to field scale
        """
        assert self.field1.scale == self.field2.scale == self.scale

    @property
    def expression(self) -> SympyOperator:
        """Returns bilinear as operator expression."""
        return self.field1.expression * self.matrix1 * self.field2.expression


# class ThreeFieldOperator(Operator):
#     field1
#     matrix1
#     field2
#     matrix2
#     field3
#
#
class FourFieldOperator(Operator):
    """Bilinear field operator table.

    TODO: choices for matrix field?
    """

    field1 = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        help_text="Conjugated field present on the left of the operator expression"
        " (e.g., Bar(u)).",
        related_name="operators_41",
    )
    matrix1 = SympyField(
        encoder="non-commutative-expression",
        help_text="Term representing the spin operator between field one and two."
        " For example $\\gamma_5$",
    )
    field2 = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        help_text="Second field (from left) of the operator expression (e.g., d).",
        related_name="operators_42",
    )
    matrix2 = SympyField(
        encoder="non-commutative-expression",
        help_text="Term representing the spin operator between field two and three",
    )
    field3 = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        help_text="Third field (from left) of the operator expression (e.g., d)..",
        related_name="operators_43",
    )
    matrix3 = SympyField(
        encoder="non-commutative-expression",
        help_text="Term representing the spin operator between field three and four",
    )
    field4 = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        help_text="Last field (e.g., on the right side) of the operator expression.",
        related_name="operators_44",
    )

    class Meta:
        """Implments unique constraint."""

        unique_together = [
            "field1",
            "matrix1",
            "field2",
            "matrix2",
            "field3",
            "matrix3",
            "field4",
        ]

    def check_consistency(self):
        """Checks operator properties.

        Tests in order:
        1. Fields are specified at the same scale
        2. Own scale is equal to field scale
        """
        assert (
            self.field1.scale
            == self.field2.scale
            == self.field3.scale
            == self.field4.scale
            == self.scale
        )

    @property
    def expression(self) -> SympyOperator:
        """Returns bilinear as operator expression."""
        return (
            self.field1.expression
            * self.matrix1
            * self.field2.expression
            * self.matrix2
            * self.field3.expression
            * self.matrix3
            * self.field4.expression
        )
