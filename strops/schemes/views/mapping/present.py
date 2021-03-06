"""Views associated wit presenting operator mappings."""
from typing import Dict, Any, Optional
from collections import defaultdict

from django.http import Http404
from django.views.generic import TemplateView

from strops.operators.forms import NotRequiredOperatorFactorForm
from strops.operators.models import Operator
from strops.schemes.models import ExpansionScheme
from strops.schemes.utils.graphs import get_connected_operators, get_all_paths
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

    def get_formset(self, schemes, data: Optional[Dict[str, Any]] = None):
        source_ops = Operator.objects.filter(
            id__in=schemes[0].relations.values_list("source__id", flat=True)
        )
        formset = formset_factory(
            NotRequiredOperatorFactorForm,
            extra=0,
            min_num=len(source_ops),
            max_num=len(source_ops),
        )(data=data, initial=[{"operator": operator} for operator in source_ops])
        return formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Specify the source Lagrangian"
        context["schemes"] = kwargs.get("schemes") or self.get_schemes()
        context["branch"] = self.get_branch(context["schemes"])
        context["connected_operators"] = kwargs.get(
            "connected_operators"
        ) or get_connected_operators(context["schemes"])
        context["connection_graph"] = get_op_connections_graph_plotly(
            context["schemes"],
            context["connected_operators"],
            font_size=14,
            font_family=None,
            height=800,
            margin=dict(l=150, r=150, t=100, b=100),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        context["formset"] = kwargs.pop("formset", None) or self.get_formset(
            context["schemes"]
        )
        context.update(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(self.get_schemes(), request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.render_to_response(self.get_context_data(formset=formset))

    def form_valid(self, formset):
        """If the form is valid, redirect to the supplied URL."""
        source_lagrangian = {
            el["operator"]: el["factor"] for el in formset.cleaned_data if el["factor"]
        }

        schemes = self.get_schemes()
        connected_operators = get_connected_operators(schemes)
        operator_connections = get_all_paths(schemes, connected_operators)

        target_contributions = defaultdict(int)
        parameters = set()
        for path, steps in operator_connections.items():
            if not path[0] in source_lagrangian:
                continue
            factor = source_lagrangian[path[0]]
            for start, end, relations in steps:
                tmp = 0
                for relation in relations:
                    parameters |= set(relation.parameters.all())
                    tmp += relation.factor
                factor *= tmp

            target_contributions[end] += factor

        for op, factor in target_contributions.items():
            target_contributions[op] = factor.expand().simplify()

        source_lagrangian = sum(
            factor * operator.expression
            for operator, factor in source_lagrangian.items()
        )
        target_lagrangian = sum(
            factor * operator.expression
            for operator, factor in target_contributions.items()
        )

        par_symbols = set(par.symbol for par in parameters)
        parameters = set(
            par for par in parameters if par.symbol in target_lagrangian.free_symbols
        )
        missing_symbols = set()
        for operator, factor in target_contributions.items():
            missing_symbols |= factor.free_symbols - par_symbols

        return self.render_to_response(
            self.get_context_data(
                formset=formset,
                source_lagrangian=source_lagrangian,
                target_lagrangian=target_lagrangian,
                connected_operators=connected_operators,
                schemes=schemes,
                operator_connections=operator_connections,
                parameters=parameters,
                missing_symbols=missing_symbols,
                target_contributions=list(target_contributions.items()),
            )
        )
