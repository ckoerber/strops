"""Detail views of schemes app."""
from django.views.generic import ListView, DetailView

from strops.schemes.models import ExpansionScheme


class ExpansionSchemeListView(ListView):
    """List view of all operators."""

    model = ExpansionScheme
    template_name = "schemes/expansion_scheme_list.html"


class ExpansionSchemeDetailsView(DetailView):
    """Detail view of expansion scheme."""

    template_name = "schemes/expansion_scheme_details.html"
    model = ExpansionScheme
    context_object_name = "scheme"
