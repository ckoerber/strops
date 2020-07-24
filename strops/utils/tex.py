"""Shortcuts for latex conversions."""
from re import compile
from sympy import latex as sympy_tex

BAR_SUBS1 = compile(r"Bar\(([^\)]+)\)")
BAR_SUBS2 = compile(r"\\operatorname{Bar}{\\left\(\s*([^\s\\right\)]+)\s*\\right\)}")


def latex(expr, wrapped=(r"\(", r"\)")):
    """Wraps sympy latex for bar replacements."""
    tex = sympy_tex(expr)
    tex = BAR_SUBS1.sub(r"\\bar{\g<1>}", tex)
    tex = BAR_SUBS2.sub(r"\\bar{\g<1>}", tex)

    if wrapped:
        tex = wrapped[0] + tex + wrapped[1]
    return tex
