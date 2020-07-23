"""Utility template tags for schemes."""
from django import template
from sympy import latex


register = template.Library()


@register.simple_tag
def debug(el):
    breakpoint()
    return el


@register.filter(name="zip")
def zip_lists(a, b):
    return zip(a, b)


@register.inclusion_tag("schemes/scale_branch_formset.html")
def render_scale_branch_formset(branch, formset):
    return {"branch": branch, "formset": formset}


@register.inclusion_tag("schemes/scheme_choice_field.html")
def render_scheme_choice_field(field):
    return {"field": field}


@register.inclusion_tag("schemes/scheme_summary.html")
def summarize_scheme(scheme):
    return {"scheme": scheme}


@register.filter
def tex(expr, left=None, right=None):
    left = left or ""
    right = right or ""
    return left + latex(expr) + right
