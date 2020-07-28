"""Views for the operator app."""
from django.views.generic import ListView, DetailView

from strops.operators.models import Operator


class OperatorListView(ListView):
    """List view of all operators."""

    model = Operator
    template_name = "operator_list_view.html"


class OperatorDetailView(DetailView):
    """Detail view of operator."""

    model = Operator
    template_name = "operator_detail_view.html"
    context_name = "operator"
