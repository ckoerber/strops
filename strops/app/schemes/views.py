from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView
from django.forms import formset_factory

from django.http import Http404, HttpResponseRedirect
from strops.app.schemes.models import ExpansionScheme
from strops.app.schemes.forms import (
    ScaleForm,
    ExpansionSchemeForm,
    SCALES,
    SourceTargetScaleForm,
)
from strops.app.schemes.utils.graphs import (
    get_connected_scales,
    get_scale_branches,
    get_scales_with_connections,
)


class Index(TemplateView):
    template_name = "schemes/index.html"


class ExpansionSchemeDetailsView(DetailView):
    template_name = "schemes/expansion_scheme_details.html"
    model = ExpansionScheme
    context_object_name = "scheme"


class OpMappingIntro(TemplateView):
    template_name = "schemes/index.html"


class PickSourceScaleView(FormView):
    template_name = "simple_form.html"
    form_class = ScaleForm

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse_lazy(
                "schemes:op-mapping-target-scale",
                kwargs={"source_scale": form.cleaned_data["scale"]},
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Where do you want to start?"
        return context

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        scales = get_scales_with_connections()
        form.fields["scale"].choices = [
            (key, verbose) for key, verbose in SCALES if key in scales
        ]
        return form


class PickTargetScaleView(FormView):
    template_name = "simple_form.html"
    form_class = SourceTargetScaleForm

    def get_initial(self):
        return {"source_scale": self.kwargs["source_scale"]}

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        form = super().get_form(form_class=form_class)
        target_scales = get_connected_scales(self.kwargs["source_scale"])
        if not target_scales:
            raise Http404(
                "Could not locate scales connected to %s scale."
                % self.kwargs["source_scale"]
            )
        form.fields["target_scale"].choices = [
            (key, verbose) for key, verbose in SCALES if key in target_scales
        ]
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "At which scale do you want to evaluate operators?"
        return context

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse_lazy(
                "schemes:op-mapping-branch-select",
                kwargs={
                    "source_scale": form.cleaned_data["source_scale"],
                    "target_scale": form.cleaned_data["target_scale"],
                },
            )
        )


class PickBranchView(TemplateView):
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
        return self.render_to_response(self.get_context_data())


class DetailsView(FormView):
    template_name = "schemes/index.html"
    success_url = reverse_lazy("op-mapping-details")
