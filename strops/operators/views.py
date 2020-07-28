"""Views for the operator app."""
from django.views.generic import ListView, DetailView
from django.urls import reverse

from strops.operators.models import Operator


class OperatorListView(ListView):
    """List view of all operators."""

    model = Operator
    template_name = "operators/operator_list.html"
    fieldnames = {
        "id": "Id",
        "name": "Name",
        "n_fields": "# Fields",
        "expression_latex": "Expression",
        "lorentz": "Lorentz",
        "scale": "Scale",
        "charge": "$C$",
        "parity": "$P$",
        "time": "$T$",
    }

    def get_context_data(self, **kwargs):
        """Sets up api url and columns."""
        context = super().get_context_data(**kwargs)
        context["columns"] = self.fieldnames
        context["api_url"] = reverse("api:api-root") + "operators/?format=datatables"
        return context


class OperatorDetailView(DetailView):
    """Detail view of operator."""

    model = Operator
    template_name = "operators/operator_details.html"
    context_name = "operator"
