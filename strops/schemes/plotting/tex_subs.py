"""Subsitutions to render tex expressions in plotly."""
from re import compile

PATTERNS = [
    (compile(r"Bar\(([a-zA-Z]+)\)"), r"\g<1>"),
    (compile(r"Dagger\(([a-zA-Z]+)\)"), r"\g<1>"),
    (compile(r"gamma_5"), r"𝛄₅"),
    (compile(r"gamma"), r"𝛄"),
    (compile(r"chi"), r"𝛘"),
    (compile(r"sigma"), r"𝞂"),
    (compile(r"mu"), r"𝜇"),
    (compile(r"nu"), r"𝜈"),
    (compile(r"\_"), r""),
    (compile(r"\*"), r" "),
    (compile(r"I"), r"i"),
    (compile(r"\s+"), r""),
]


def sympy_subs(expr) -> str:
    """Substitudes sympy expressions to UTF8 characters."""
    string = str(expr)
    for pattern, replacement in PATTERNS:
        string = pattern.sub(replacement, string)
    return string
