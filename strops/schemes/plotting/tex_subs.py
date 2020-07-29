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
    (compile(r"delta"), r"𝛅"),
    (
        compile(r"epsilon_ijk[\s\*]+([a-zA-Z𝞂]+)_j[\s\*]+([a-zA-Z𝞂]+)_k"),
        r"(\g<1>⨉\g<2>)ᵢ",
    ),
    (compile(r"epsilon"), r"𝛆"),
    (compile(r"v\_i2"), r"vᵢ²"),
    (compile(r"\_i"), r"ᵢ"),
    (compile(r"\_"), r""),
    (compile(r"\*"), r" "),
    (compile(r"I"), r"i"),
    (compile(r"\s+"), r""),
    (compile(r"p"), r"𝗽"),
    (compile(r"n"), r"𝐧"),
    (compile(r"u"), r"𝐮"),
    (compile(r"d"), r"𝗱"),
]


def sympy_subs(expr) -> str:
    """Substitudes sympy expressions to UTF8 characters."""
    string = str(expr)
    for pattern, replacement in PATTERNS:
        string = pattern.sub(replacement, string)
    return string
