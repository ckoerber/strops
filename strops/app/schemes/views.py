from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from strops.app.schemes.forms import ScaleForm, BranchFormSet, OperatorFormSet, SCALES
from strops.app.schemes.utils.graphs import get_connected_scales


class Index(TemplateView):
    template_name = "schemes/index.html"


class OpMappingIntro(TemplateView):
    template_name = "schemes/index.html"


class PickSourceScaleView(FormView):
    template_name = "simple_form.html"
    form_class = ScaleForm
    scale = None

    def form_valid(self, form):
        self.scale = form.cleaned_data["scale"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "schemes:op-mapping-target-scale", kwargs={"source_scale": self.scale}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Where do you want to start?"
        return context


class PickTargetScaleView(FormView):
    template_name = "simple_form.html"
    form_class = ScaleForm
    success_url = reverse_lazy("op-mapping-branch-select")
    source_scale = None
    target_scale = None
    choices = None

    def get(self, request, *args, **kwargs):
        self.source_scale = kwargs.get("source_scale")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "At which scale do you want to evaluate operators?"
        context["source_scale"] = self.source_scale
        context["choices"] = self.choices
        return context

    def form_valid(self, form):
        self.target_scale = form.cleaned_data["scale"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "schemes:op-mapping-branch-select",
            kwargs={
                "source_scale": self.source_scale,
                "target_scale": self.target_scale,
            },
        )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        choices = get_connected_scales(self.source_scale)
        form.fields["scale"].choices = [el for el in SCALES if el[0] in choices]
        return form


class PickBranchView(FormView):
    template_name = "schemes/index.html"
    form_class = BranchFormSet
    success_url = reverse_lazy("op-mapping-details")


class DetailsView(FormView):
    template_name = "schemes/index.html"
    form_class = OperatorFormSet
    success_url = reverse_lazy("op-mapping-details")
