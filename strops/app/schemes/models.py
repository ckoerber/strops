"""Models of schemes."""
from django.db import models
from django.urls import reverse

from espressodb.base.models import Base

from sympy import sympify

from strops.app.utils.fields import SympyField
from strops.app.operators.models import SCALES, Operator
from strops.app.references.models import Publication
from strops.app.parameters.models import Parameter


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
    references = models.ManyToManyField(
        Publication, help_text="Publications specifying the operator relationship."
    )
    description = models.TextField(
        help_text="What does this scheme represent?", null=True, blank=False
    )

    def __str__(self):
        return f"ExpansionScheme({self.name})"

    def get_absolute_url(self):
        return reverse("schemes:expansion_scheme_detail", args=[str(self.id)])

    def related_source_operators(self):
        ids = self.relations.values_list("source__id", flat=True)
        return Operator.objects.filter(id__in=ids)

    def related_target_operators(self):
        ids = self.relations.values_list("target__id", flat=True)
        return Operator.objects.filter(id__in=ids)

    def orders(self):
        return self.relations.values_list("expansionorder__power", flat=True)


class ExpansionParameter(Base):
    """Unitless parameter used for power counting in operator expansion scheme."""

    name = models.CharField(max_length=256, help_text="Name of the parameter scheme.")
    symbol = SympyField(
        encoder="symbol", help_text="Symbol representing this parameter."
    )
    scheme = models.ForeignKey(
        ExpansionScheme, on_delete=models.CASCADE, related_name="expansion_parameters"
    )
    description = models.TextField(
        help_text="What does this parameter describe, which assumptions are made?"
    )
    natural_size = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Estimate of parameter size under 'regular' conditions.",
    )

    class Meta:
        """Constraints for parameter."""

        constraints = [
            models.UniqueConstraint(
                fields=["name", "scheme"], name="Unique name and scheme"
            ),
            models.UniqueConstraint(
                fields=["scheme", "symbol"], name="Unique symbol and scheme"
            ),
        ]

    def __str__(self):
        """Verbose name of parameter."""
        return f"{self.symbol} ({self.scheme.name})"


class OperatorRelation(Base):
    """Table storing information between different oprator representation bridging scales.

    For example, this quark operator maps to the following nucleon operators:

    ``source = Bar(q) * q -> target * factor`` at ``order``
     (where order is present in the factor.)
    """

    source = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
        related_name="source_for",
        help_text="More fundamental operator as a source for the propagation of scales.",
    )
    target = models.ForeignKey(
        Operator,
        on_delete=models.CASCADE,
        related_name="target_of",
        help_text="Operator as a source for the propagation of scales.",
    )
    factor = SympyField(
        encoder="expression",
        help_text="Factor associated with the propagation of scales."
        " E.g., 'source -> factor * target' at 'order'.",
    )
    scheme = models.ForeignKey(
        ExpansionScheme,
        on_delete=models.CASCADE,
        related_name="relations",
        help_text="Key for grouping different schemes to form a complete representation"
        " (e.g., if an expansion scheme is workout over several publications)."
        " Relationships with the same tag should share the same 'order' keys"
        " to allow sorting them by relevance. ",
    )
    order = models.ManyToManyField(
        ExpansionParameter,
        through="ExpansionOrder",
        help_text="Information allowing to order different operators"
        " by their relevance."
        " E.g., chiral power counting scheme.",
    )
    parameters = models.ManyToManyField(
        Parameter,
        help_text="Non-expansion paramters present in the factor.",
        blank=True,
    )
    references = models.ManyToManyField(
        Publication, help_text="Publications specifying the operator relationship."
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
            raise ValueError("Target operator not at same scale as scheme specifies.")
        if self.source.scale != self.scheme.source_scale:
            raise ValueError("Source operator not at same scale as scheme specifies.")


class ExpansionOrder(Base):
    """Through table for relating expanion parameters to operator expansions."""

    parameter = models.ForeignKey(
        ExpansionParameter,
        on_delete=models.CASCADE,
        help_text="The expansion parameter for relating different operators.",
    )
    relation = models.ForeignKey(
        OperatorRelation,
        on_delete=models.CASCADE,
        help_text="The relation between operators at different scales.",
    )
    power = models.IntegerField(
        help_text="The power of the expansion paramter in given relation."
    )
