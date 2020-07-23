"""Views asociated with picking scales for operator mappings."""
from django.views.generic.edit import FormView
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from strops.app.schemes.forms import ScaleForm, SCALES, SourceTargetScaleForm
from strops.app.schemes.utils.graphs import (
    get_connected_scales,
    get_scales_with_connections,
)


class PickSourceScaleView(FormView):
    """Select source scale view."""

    template_name = "simple_form.html"
    form_class = ScaleForm

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse(
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
    """Select target scale view for given source scale."""

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
            reverse(
                "schemes:op-mapping-branch-select",
                kwargs={
                    "source_scale": form.cleaned_data["source_scale"],
                    "target_scale": form.cleaned_data["target_scale"],
                },
            )
        )
