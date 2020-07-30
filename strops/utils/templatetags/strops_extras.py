"""Utility template tags for schemes."""
from typing import List, Optional
from django import template
from subprocess import check_output
from os import path

from strops.config.settings import ROOT_DIR
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


@register.simple_tag
def get_version() -> Optional[str]:
    """Returns the current version of strops.

    Requires a symlink install or to run strops directly from the repository.
    """
    commit = None
    try:
        git_dir = path.join(ROOT_DIR, ".git")
        if path.exists(git_dir):
            commit = (
                check_output(["git", f"--git-dir={git_dir}", "describe", "--always"])
                .strip()
                .decode()
            )
    except Exception:
        pass
    return commit
