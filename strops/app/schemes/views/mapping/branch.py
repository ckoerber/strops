"""View for selecting a certain branch for bridging scales."""
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.forms import formset_factory

from strops.app.schemes.forms import SCALES, ExpansionSchemeForm
from strops.app.schemes.utils.graphs import get_scale_branches


class PickBranchView(TemplateView):
    """View for selecting a certain branch for bridging scales."""

    template_name = "schemes/branch-select-view.html"

    def get_branches(self):
        source = self.kwargs["source_scale"]
        target = self.kwargs["target_scale"]
        for scale in (source, target):
            if not scale or scale not in [s for s, l in SCALES]:
                raise Http404("No views for scale %s." % scale)
        return get_scale_branches(source, target, instance_as_key=True)

    def get_formsets(self):
        formsets = {}
        for branch, steps in self.get_branches().items():
            formsets[branch] = formset_factory(ExpansionSchemeForm, extra=0)(
                initial=[
                    {"source_scale": source, "target_scale": target, "scheme": schemes}
                    for source, target, schemes in steps
                ],
                prefix="branch_%s" % "_".join(branch),
            )
        return formsets

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Which expansion schemes do you want to use?"
        context["source_scale"] = self.kwargs["source_scale"]
        context["target_scale"] = self.kwargs["target_scale"]
        context["formsets"] = kwargs.get("formsets") or self.get_formsets()
        return context

    def post(self, request, *args, **kwargs):
        submitted_branch = request.POST.get("branch")
        key = tuple(submitted_branch.replace("branch_", "").split("_"))
        formset = formset_factory(ExpansionSchemeForm, extra=0)(
            request.POST, prefix=submitted_branch
        )
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            formsets = self.get_formsets()
            formsets[key] = formset
            return self.render_to_response(self.get_context_data(formsets=formsets))

    def form_valid(self, formset):
        """If the form is valid, redirect to the supplied URL."""
        scheme_ids = [str(el["scheme"].id) for el in formset.cleaned_data]
        return redirect(
            reverse("schemes:op-mapping-present") + "?schemes=" + ",".join(scheme_ids)
        )
