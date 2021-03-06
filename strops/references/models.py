"""Models of references."""
from typing import Optional

from django.db import models
from espressodb.base.models import Base


class Publication(Base):
    """Publication as a reference for specifying information about operators."""

    arxiv_id = models.CharField(
        max_length=20,
        help_text="Arxiv qualifier like '2000.01234'.",
        null=True,
        blank=True,
    )
    inspirehep_id = models.IntegerField(
        help_text="Insprie HEP id (inspirehep.net/literature/{id}).", unique=True,
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
    preprint_date = models.DateField(
        help_text="Date preprint got uploaded.", null=True, blank=True
    )
    misc = models.JSONField(
        null=True, blank=True, help_text="Additional optional information."
    )

    def __str__(self):
        """Returns arxiv qualifier."""
        return (
            f"[{self.arxiv_id}]"
            if self.arxiv_id
            else f"Inspirehep({self.inspirehep_id})"
        )

    @property
    def inspire_api_url(self) -> str:
        """Returns link to inspire.net."""
        return f"https://inspirehep.net/api/literature/{self.inspirehep_id}"

    @property
    def inspire_url(self) -> str:
        """Returns link to inspire.net."""
        return f"https://inspirehep.net/literature/{self.inspirehep_id}"

    @property
    def arxiv_url(self) -> Optional[str]:
        """Returns link to arxiv."""
        return f"https://arxiv.org/abs/{self.arxiv_id}" if self.arxiv_id else None

    @property
    def url(self) -> str:
        return self.arxiv_url or self.inspire_url
