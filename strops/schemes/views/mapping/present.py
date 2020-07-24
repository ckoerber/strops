"""Views associated wit presenting operator mappings."""
from django.http import Http404
from django.views.generic import TemplateView

from strops.operators.forms import OperatorFactorForm
from strops.operators.models import Operator
from strops.schemes.models import ExpansionScheme
from strops.schemes.utils.graphs import get_connected_operators
from strops.schemes.plotting.connections import get_op_connections_graph_plotly
from django.forms import formset_factory


class PresentView(TemplateView):
    """View associated wit presenting operator mappings."""

    template_name = "schemes/present.html"

    def get_schemes(self):
        """Extract and verify schemes from url query parameters."""
        data = self.request.GET or self.request.POST
        scheme_ids = data["schemes"].split(",") if "schemes" in data else None

        if not scheme_ids:
            raise Http404("URL scheme parameter must be a list or a single id.")

        schemes = []
        for idx in scheme_ids:
            scheme = ExpansionScheme.objects.filter(id=idx).first()
            if not scheme:
                raise Http404("Could not locate scheme for id %s." % idx)
            schemes.append(scheme)

        if len(schemes) > 1:
            prev_scheme = schemes[0]
            for scheme in schemes[1:]:
                if not prev_scheme.target_scale == scheme.source_scale:
                    raise Http404(
                        "Scheme %s not connected to %s" % (prev_scheme, scheme)
                    )
                prev_scheme = scheme

        return schemes

    def get_branch(self, schemes):
        branch = []
        for scheme in schemes:
            branch.append(scheme.source_scale)
        branch.append(scheme.target_scale)
        return branch

    def get_formset(self, schemes):
        source_ops = Operator.objects.filter(
            id__in=schemes[0].relations.values_list("source__id", flat=True)
        )
        formset = formset_factory(
            OperatorFactorForm,
            extra=0,
            min_num=len(source_ops),
            max_num=len(source_ops),
        )(initial=[{"operator": operator} for operator in source_ops])
        return formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Specify the source Lagrangian"
        context["schemes"] = self.get_schemes()
        context["branch"] = self.get_branch(context["schemes"])
        context["connected_operators"] = get_connected_operators(context["schemes"])
        context["connection_graph"] = get_op_connections_graph_plotly(
            context["schemes"],
            context["connected_operators"],
            font_size=20,
            font_family=None,
            margin=dict(l=150, r=150, t=100, b=100),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        context["formset"] = kwargs.get("formset") or self.get_formset(
            context["schemes"]
        )
        return context
