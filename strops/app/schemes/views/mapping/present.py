"""Views associated wit presenting operator mappings."""
from django.views.generic import TemplateView


class PresentView(TemplateView):
    """View associated wit presenting operator mappings."""

    template_name = "schemes/index.html"
