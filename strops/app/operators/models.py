"""Table implementations related to operators."""
from django.db import models
from espressodb.base.models import Base

from sympy import sympify, Function
from sympy.physics.quantum import Operator as SympyOperator


from strops.app.utils.fields import SympyField


SCALES = [
    ("quark", "Quark"),
    ("nucleon", "nucleon"),
    ("nucleon-nr", "Non-relativistic nuclear scale"),
]


class Field(Base):
    """Field representing a degree of freedom present in operators."""

    kind = models.CharField(
        max_length=256,
        choices=SCALES,
        help_text="Kind of operator like 'quark'  or 'nucleon'.",
    )
    name = models.CharField(
        max_length=256, help_text="Descriptive name like 'up quark' or 'proton'."
    )
    label = models.CharField(
        max_length=256,
        help_text="Which version of d.o.f., e.g.,"
        " specifying flavor ('up') or strong isospin ('proton').",
    )
    symbol = SympyField(
        encoder="Operator", help_text="Mathematical symbol representing the d.o.f.",
    )
    conjugation_method = models.CharField(
        null=True,
        blank=True,
        default="Dagger",
        max_length=20,
        choices=[("Dagger", "Dagger"), ("Bar", "Bar"), (None, "None")],
        help_text="Number of field occurances.",
    )

    class Meta:
        """Constraints on class."""

        unique_together = ["kind", "label"]

    @property
    def conjugate(self):
        """Returns conjugated field (e.g., Dagger(psi))."""
        return (
            Function(self.conjugation_method)(self.symbol)
            if self.conjugation_method is not None
            else self.symbol
        )

    def __str__(self):
        """Returns own name."""
        return self.name


class BilinearOperator(Base):
    r"""Operator evaluated in strong interaction matrix elements.

    Implements $\\psi^\\dagger O \\psi$

    Includes spin and chirality, does not include factors and isospin/flavor
    """

    name = models.CharField(
        max_length=256, help_text="Name of the operator which can be used for searches."
    )
    field_lhs = models.ForeignKey(
        Field,
        help_text="Conjugated field present on the left of the operator expression"
        " (e.g., Bar(u)).",
    )
    matrix = SympyField(
        encoder="operator",
        unique=True,
        help_text="Term representing the operator. For example $\\gamma_5$",
    )
    field_rhs = models.ForeignKey(
        Field,
        help_text="Field present on the right of the operator expression (e.g., d).",
    )
    kind = models.CharField(
        choices=[
            ("s", "Scalar"),
            ("v", "Vector"),
            ("ps", "Pseudo Scalar"),
            ("pv", "Pseudo Vector"),
            ("t", "Tensor"),
            ("pt", "Pseudo Tensor"),
        ],
        max_length=2,
        help_text="Which kind of spin interactions describe this operator?",
    )
    # discrete symmetries
    charge = models.IntegerField(
        help_text="Charge transformation behavior of operator."
    )
    parity = models.IntegerField(
        help_text="Parity transformation behavior of operator."
    )
    time = models.IntegerField(help_text="Time transformation behavior of operator.")
    # Further details
    details = models.JSONField(
        null=True,
        blank=True,
        help_text="Further optional information to specify the operator.",
    )

    def expression(self) -> SympyOperator:
        r"""Returns $\\psi^\\dagger O \\psi$."""
        return self.field_lhs.conjugate * self.matrix * self.field_rhs

    def __str__(self):
        """Returns expression."""
        return f"{self.field_lhs} {self.expression}"

    def check_consistency(self):
        """Checks that in and out field are at the same scale."""
        assert self.field_lhs.kind == self.field_rhs.kind

    @property
    def scale(self):
        """Returns the scale at which the operator is implemented defined by fields.

        Returns kind of first field (all fields are at the same scale).
        """
        return self.field_lhs.kind


class Publication(Base):
    """Publication as a reference for specifying information about operators."""

    arxiv_id = models.CharField(
        max_length=20, help_text="Arxiv qualifier like '2000.01234'."
    )
    authors = models.TextField(
        help_text="Authors of the reference as comma seperated list."
    )
    title = models.CharField(max_length=256, help_text="Title of the publication.")
    journal = models.CharField(
        null=True,
        blank=True,
        max_length=256,
        help_text="Journal qualifier of the publication.",
    )
    url = models.URLField(
        null=True,
        blank=True,
        help_text="Link to access the publication, e.g., inspirehep.net link.",
    )
    misc = models.JSONField(
        null=True, blank=True, help_text="Additional optional information."
    )

    def __str__(self):
        """Returns arxiv qualifier."""
        return f"[{self.arxiv_id}]"


class ExpansionScheme(Base):
    """An expansion scheme which relates operators at different scales.

    It must provides keys which allow ordering different opator relations.
    """

    name = models.CharField(max_length=256, help_text="Name of the expansion scheme.")
    source_scale = models.CharField(
        max_length=256, choices=SCALES, help_text="The source scale of the expansion."
    )
    target_scale = models.CharField(
        max_length=256, choices=SCALES, help_text="The target scale of the expansion."
    )
    parameters = models.JSONField(
        help_text="List of expansion parameters which must be present for"
        " each term (OperatorRelation) in the expansion."
    )
    references = models.ManyToManyField(
        Publication, help_text="Publications specifying the operator relationship."
    )

    def check_consistency(self):
        """Checks if parameters key is a list of sympy expressions."""
        assert isinstance(self.parameters, list)
        for par in self.parameters:
            sympify(par)


class Parameter(Base):
    """Parameters used in computation.

    This class specifies numerical values to extract from parameters.

    Todo:
        Update docstrings and consistency checks.
    """

    name = models.CharField(
        max_length=256, help_text="Descriptive name of the variable"
    )
    symbol = SympyField(
        encoder="Symbol", help_text="The mathematical symbol (Sympy syntax)",
    )
    value = models.JSONField(help_text="Value or descriptive information.")
    reference = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        help_text="Publication specifying the parameter.",
    )

    class Meta:
        """Implements unique constraint on name anmd reference."""

        unique_together = ["name", "reference"]

    def __str__(self):
        """Returns own name and reference string."""
        return f"{self.name} ({self.reference})"


class BilinearOperatorRelation(Base):
    """Table storing information between different oprator representation bridging scales.

    For example, this quark operator maps to the following nucleon operators.
    """

    source = models.ForeignKey(
        BilinearOperator,
        on_delete=models.CASCADE,
        related_name="source_for",
        help_text="More fundamental operator as a source for the propagation of scales.",
    )
    target = models.ForeignKey(
        BilinearOperator,
        on_delete=models.CASCADE,
        related_name="target_of",
        help_text="Operator as a source for the propagation of scales.",
    )
    factor = SympyField(
        encoder="expression",
        help_text="Factor associated with the propagation of scales."
        " E.g., 'source -> factor * target' at 'order'.",
    )
    order = models.JSONField(
        null=True,
        blank=True,
        help_text="Additional information allowing to order different operators"
        " by their relevance."
        " E.g., chiral power counting scheme.",
    )
    references = models.ManyToManyField(
        Publication, help_text="Publications specifying the operator relationship."
    )
    scheme = models.ForeignKey(
        ExpansionScheme,
        on_delete=models.CASCADE,
        help_text="Key for grouping different schemes to form a complete representation"
        " (e.g., if an expansion scheme is workout over several publications)."
        " Relationships with the same tag should share the same 'order' keys"
        " to allow sorting them by relevance. ",
    )
    parameters = models.ManyToManyField(
        Parameter, help_text="Parameter present in the expression."
    )

    def check_consistency(self):
        """Runs consistency checks on operator relation.

        Checks:
            * factor can be converted to sympy expression
            * target scale equals scheme target scale
            * source scale equals scheme source scale
            * all expansion parameters defined by scheme are present
        """
        sympify(self.factor)

        if self.target.scale != self.scheme.target_scale:
            raise ValueError
        if self.source.scale != self.scheme.source_scale:
            raise ValueError

        if not set(self.order.keys()) != set(self.scheme.parameters):
            raise ValueError
