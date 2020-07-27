"""Utility template tags for schemes."""
from typing import List
from django import template

from strops.operators.models import SCALES as _SCALES
from strops.utils.tex import latex

register = template.Library()

SCALES = {key: val for key, val in _SCALES}


@register.filter
def tex(expr, left=None, right=None):
    left = left or ""
    right = right or ""
    return latex(expr, wrapped=(left, right))


@register.simple_tag
def debug(el):
    breakpoint()
    return el


@register.filter(name="zip")
def zip_lists(a, b):
    return zip(a, b)


@register.filter
def map_title(strings: List[str]) -> List[str]:
    return [str(el).capitalize() for el in strings]
