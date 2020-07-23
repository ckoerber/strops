"""Views associated wit presenting operator mappings."""
from django.http import Http404
from django.views.generic import TemplateView

from strops.app.schemes.models import ExpansionScheme


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Specify the source Lagrangian"
        context["schemes"] = self.get_schemes()
        branch = []
        for scheme in context["schemes"]:
            branch.append(scheme.source_scale)
        branch.append(scheme.target_scale)
        context["branch"] = branch
        # context["formsets"] = kwargs.get("formsets") or self.get_formsets()
        return context
