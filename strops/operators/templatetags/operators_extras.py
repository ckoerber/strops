"""Utility template tags for schemes."""
from typing import List
from django import template

from strops.operators.models import Operator
from strops.operators.models import SCALES as _SCALES

register = template.Library()

SCALES = {key: val for key, val in _SCALES}


@register.filter
def scale_name(scale: str) -> str:
    return SCALES.get(scale, "")


@register.filter
def map_scale_names(scales: List[str]) -> List[str]:
    return [SCALES.get(scale) for scale in scales]


@register.inclusion_tag("operators/opertor_factor_form.html")
def render_opertor_factor_form(form):
    return {"form": form}


@register.simple_tag
def get_op(obj):
    if isinstance(obj, str) and obj.isnumeric():
        obj = int(obj)
    if isinstance(obj, Operator):
        return obj
    elif isinstance(obj, int):
        return Operator.objects.get(id=obj)
    elif obj is None:
        return None
    else:
        raise TypeError(f"Could not infer operator from {obj}")
