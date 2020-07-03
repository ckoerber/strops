"""Implementation of fields special to strops.

Provides:
    * Sympy field
"""
from typing import Optional, Union

from django.db.models import TextField

from sympy import sympify, Symbol, SympifyError, Expr
from sympy.physics.quantum import Operator
from sympy.parsing.sympy_parser import parse_expr


def non_commutative_sympify(string: str):
    """Evaluates sympy string in non-commutative fashion.

    This function was taken from stack overflow answer by @ely
    https://stackoverflow.com/a/32169940
    """
    parsed_expr = parse_expr(string, evaluate=False)

    new_locals = {
        sym.name: Symbol(sym.name, commutative=False)
        for sym in parsed_expr.atoms(Symbol)
    }

    return sympify(string, locals=new_locals)


ENCODERS = {
    "expression": sympify,
    "symbol": Symbol,
    "operator": Operator,
    "non-commutative-expression": non_commutative_sympify,
}


class SympyField(TextField):
    """Field which stores sympy expressions as TextFields.

    Warning:
        This field uses sympify expressions under the hood.
        Thus potentially harmful code will be evaluated using `eval`.
        Do not use this field if you do not trust the input source.
    """

    description = "Sympy"

    def __init__(
        self, *args, encoder: str = "expression", **kwargs,
    ):
        """Overloads default TextField by providing sympy version.

        Stores encoder used to convert string to sympy expression.
        """
        if encoder not in ENCODERS:
            raise KeyError(f"Encoder must be one out of {ENCODERS.keys()}")
        self.encoder = encoder
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """Deconstructs sumpy field by adding the encoder parameter."""
        name, path, args, kwargs = super().deconstruct()
        kwargs["encoder"] = self.encoder
        return name, path, args, kwargs

    def get_prep_value(self, value: Expr) -> Optional[str]:
        """Dumps expression to string."""
        if value is None:
            return value
        elif isinstance(value, Expr):
            return str(value)
        else:
            raise TypeError(
                f"Value must be either Expr type or None. Got {type(value)}"
            )

    def value_to_string(self, obj: Expr) -> str:
        """Serializes object by calling `get_prep_value`."""
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def from_db_value(
        self, value: Optional[str], expression, connection
    ) -> Optional[Expr]:
        """Converts db entry (string or None) to expression or None."""
        if value is None:
            return value
        try:
            encoder = ENCODERS[self.encoder]
            return encoder(value)
        except (SympifyError, KeyError):
            return value

    def to_python(self, value: Union[None, str, Expr]) -> Expr:
        """Converts value (string, None, or expression) to sympy expression."""
        if value is None:
            return value
        elif isinstance(value, Expr):
            return value
        elif isinstance(value, str):
            encoder = ENCODERS[self.encoder]
            return encoder(value)
        else:
            raise TypeError(
                f"Value must be either Expr type or None. Got {type(value)}"
            )
