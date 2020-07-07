"""Models of references."""
from django.db import models
from espressodb.base.models import Base


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
