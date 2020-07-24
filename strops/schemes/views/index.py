"""Index view of schemes app."""
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index view of schemes app."""

    template_name = "schemes/index.html"
