from django.shortcuts import redirect
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
