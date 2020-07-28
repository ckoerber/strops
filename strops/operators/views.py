"""Views for the operator app."""
from django.views.generic import ListView, DetailView

from strops.operators.models import Operator


class OperatorListView(ListView):
    """List view of all operators."""

    model = Operator
    template_name = "operators/operator_list.html"


class OperatorDetailView(DetailView):
    """Detail view of operator."""

    model = Operator
    template_name = "operators/operator_details.html"
    context_name = "operator"
