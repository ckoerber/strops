"""Detail views of schemes app."""
from django.views.generic import ListView, DetailView

from strops.operators.models import Operator
from strops.schemes.models import ExpansionScheme
from strops.schemes.utils.graphs import get_connected_operators
from strops.schemes.plotting.connections import get_op_connections_graph_plotly


class ExpansionSchemeListView(ListView):
    """List view of all operators."""

    model = ExpansionScheme
    template_name = "schemes/expansion_scheme_list.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["model"] = self.model.__doc__
        return context


class ExpansionSchemeDetailsView(DetailView):
    """Detail view of expansion scheme."""

    template_name = "schemes/expansion_scheme_details.html"
    model = ExpansionScheme
    context_object_name = "scheme"

    def get_context_data(self, **kwargs):
        scheme = kwargs.get("object")
        context = super().get_context_data()
        context["connected_operators"] = get_connected_operators([scheme])
        context["connection_graph"] = get_op_connections_graph_plotly(
            [scheme],
            context["connected_operators"],
            font_size=20,
            font_family=None,
            margin=dict(l=150, r=150, t=100, b=100),
            height=800,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        context["source_operators"] = Operator.objects.filter(
            source_for__scheme=scheme
        ).distinct()
        context["target_operators"] = Operator.objects.filter(
            target_of__scheme=scheme
        ).distinct()

        return context

        context["connected_operators"] = kwargs.get(
            "connected_operators"
        ) or get_connected_operators(context["schemes"])
