"""Index view of operator mappings."""
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index view of operator mappings."""

    template_name = "schemes/index.html"
