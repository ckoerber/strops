"""Models of parameters."""
from django.db import models
from espressodb.base.models import Base

from strops.utils.fields import SympyField
from strops.references.models import Publication
from strops.parameters.utils import format_gvar


class Parameter(Base):
    """Parameters used in computation.

    This class specifies numerical values to extract from parameters.
    """

    name = models.CharField(
        max_length=256, help_text="Descriptive name of the variable"
    )
    symbol = SympyField(
        encoder="expression", help_text="The mathematical symbol (Sympy syntax)",
    )

    class Meta:
        """Implements unique constraint on name anmd reference."""

        unique_together = ["name", "symbol"]

    def __str__(self):
        """Returns own name and reference string."""
        return f"{self.symbol} ({self.name})"


class ParameterValue(Base):
    """Value for parameter used in computation.

    Assumes uncorrelated normal distributions.
    """

    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        help_text="The abstract instance of the parameter.",
        related_name="values",
    )
    mean = models.FloatField(null=False, help_text="Mean value of parameter.")
    sdev = models.FloatField(
        null=True, blank=True, help_text="Standard deviation of parameter."
    )
    unit = models.CharField(
        max_length=10, null=True, blank=True, help_text="Unit of parameter.",
    )
    reference = models.ForeignKey(
        Publication,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Publication specifying the parameter.",
    )

    class Meta:  # noqa
        unique_together = ["parameter", "reference"]

    def __str__(self):
        """Prints string representing parameter."""
        value = format_gvar(self.mean, self.sdev) if self.sdev else str(self.mean)
        return f"{value} [{self.unit}]" if self.unit else value
