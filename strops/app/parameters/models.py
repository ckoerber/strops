"""Models of parameters."""
from django.db import models
from espressodb.base.models import Base

from strops.app.utils.fields import SympyField
from strops.app.references.models import Publication


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
        encoder="expression", help_text="The mathematical symbol (Sympy syntax)",
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
