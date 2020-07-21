from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import TemplateView

from strops.app.schemes.forms import ScaleForm, BranchFormSet, OperatorFormSet


class Index(TemplateView):
    template_name = "schemes/index.html"


class OpMappingIntro(TemplateView):
    template_name = "schemes/index.html"


class PickStartScaleView(FormView):
    template_name = "schemes/index.html"
    form_class = ScaleForm
    success_url = reverse_lazy("")


class PickTargetScaleView(FormView):
    template_name = "schemes/index.html"
    form_class = ScaleForm
    success_url = reverse_lazy("")


class PickBranchView(FormView):
    template_name = "schemes/index.html"
    form_class = BranchFormSet
    success_url = reverse_lazy("")


class PresentView(FormView):
    template_name = "schemes/index.html"
    form_class = OperatorFormSet
    success_url = reverse_lazy("")
