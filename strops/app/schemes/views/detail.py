"""Detail views of schemes app."""
from django.views.generic import DetailView

from strops.app.schemes.models import ExpansionScheme


class ExpansionSchemeDetailsView(DetailView):
    """Detail view of expansion scheme."""

    from django.views.generic import TemplateView

    template_name = "schemes/expansion_scheme_details.html"
    model = ExpansionScheme
    context_object_name = "scheme"
