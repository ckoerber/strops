"""Views for the strops app."""
from django.views.generic import TemplateView


class AboutPhysicsView(TemplateView):
    """Static view describing the phyiscs motivation."""

    template_name = "physics-about.html"
