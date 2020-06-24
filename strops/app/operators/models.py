"""Models of operators
"""

# Note: if you want your models to use espressodb features, they must inherit from Base

from django.db import models
from espressodb.base.models import Base


class DOF(Base):
    """Degrees of freedom present in operators."""

    # verbose_name = "Degree of freedom"
    kind = models.CharField(
        max_length=256, help_text="Kind of operator like 'quark'  or 'nucleon'."
    )
    name = models.CharField(
        max_length=256, help_text="Descriptive name like 'up quark' or 'proton'."
    )
    label = models.CharField(
        max_length=256,
        help_text="Which version of d.o.f., e.g.,"
        " specifying flavor ('up') or strong isospin ('proton').",
    )

    class Meta:
        """Constraints on class."""

        unique_together = ["kind", "label"]


class Operator(Base):
    """Operator evaluated in strong interaction matrix elements.

    Includes spin and chirality, does not include factors and isospin/flavor
    """

    name = models.CharField(max_length=256)
    dof = models.ManyToManyField(DOF)
    n_dofs = models.PositiveIntegerField()
    expression = models.TextField(
        unique=True,
        help_text="Fully qualified term discribing operator"
        " including creation and annihilation operators.",
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
    parity = models.IntegerField()
    time = models.IntegerField()
    charge = models.IntegerField()
    # Further details
    # details = models.JSONField()

    def __str__(self):
        """Returns expression."""
        return self.expression


class Reference(Base):
    """
    """

    arxiv_id = models.CharField(max_length=20)
    authors = models.TextField()
    journal = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    # misc = models.JSONField()


class OperatorRelation(Base):

    source = models.ForeignKey(
        Operator, on_delete=models.CASCADE, related_name="source_for"
    )
    target = models.ForeignKey(
        Operator, on_delete=models.CASCADE, related_name="target_of"
    )
    factor = models.TextField()
    references = models.ManyToManyField(Reference)
    scheme = models.CharField(max_length=256)
    # order = models.JSONField()
