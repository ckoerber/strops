"""Utility template tags for schemes."""
from typing import List
from django import template

from strops.operators.models import SCALES as _SCALES

register = template.Library()

SCALES = {key: val for key, val in _SCALES}


@register.filter
def scale_name(scale: str) -> str:
    return SCALES.get(scale, "")


@register.filter
def map_scale_names(scales: List[str]) -> List[str]:
    return [SCALES.get(scale) for scale in scales]
