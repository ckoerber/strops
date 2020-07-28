"""Detail views of schemes app."""
from django.views.generic import ListView, DetailView

from strops.schemes.models import ExpansionScheme


class ExpansionSchemeListView(ListView):
    """List view of all operators."""

    model = ExpansionScheme
    template_name = "schemes/expansion_scheme_list.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["model"] = self.model.__doc__
        print(context)
        return context


class ExpansionSchemeDetailsView(DetailView):
    """Detail view of expansion scheme."""

    template_name = "schemes/expansion_scheme_details.html"
    model = ExpansionScheme
    context_object_name = "scheme"
