"""Utility template tags for schemes."""
from django import template


register = template.Library()


@register.simple_tag
def string_join(delimeter, strings):
    return delimeter.join(strings)


@register.simple_tag
def debug(el):
    breakpoint()
    return el


@register.filter(name="zip")
def zip_lists(a, b):
    return zip(a, b)
