"""Forms for the operators app."""
from django import forms

from sympy import sympify

from strops.operators.models import Operator
from strops.utils.fields import FACTOR_VALIDATORS
from strops.utils.tex import latex


class OperatorFactorForm(forms.Form):
    factor = forms.CharField(
        max_length=400,
        help_text="What is the factor for this operator?"
        " Allowed are characters, underscore, numbers, times and divide.",
        validators=FACTOR_VALIDATORS,
    )
    operator = forms.ModelChoiceField(
        queryset=Operator.objects.all(),
        help_text="Which operator?",
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        operator = kwargs.get("initial", {}).get("operator")
        self.fields["factor"].label = (
            latex(operator.expression).replace("*", "") if operator else ""
        )
        self.fields["factor"].widget.attrs["placeholder"] = "1"

    def clean_factor(self):
        """Only allow [a-zA-Z0-9_] and single / or  *  but not powers.

        Note that `100 * * 100` is also rendered to powers.

        This is because 100 ** 100 ** 100 can be malicious
        """
        # Validators are already run
        data = self.cleaned_data["factor"]

        try:
            data = sympify(data)
        except Exception as e:
            raise forms.ValidationError(
                "Failed to sympify %s with error %s" % (data, e)
            )

        return data


class NotRequiredOperatorFactorForm(OperatorFactorForm):
    factor = forms.CharField(
        max_length=400,
        help_text="What is the factor for this operator?"
        " Allowed are characters, underscore, numbers, times and divide.",
        validators=FACTOR_VALIDATORS,
        required=False,
    )

    def clean_factor(self):
        """Only allow [a-zA-Z0-9_] and single / or  *  but not powers.

        Note that `100 * * 100` is also rendered to powers.

        This is because 100 ** 100 ** 100 can be malicious
        """
        data = self.cleaned_data["factor"]
        if data:
            data = super().clean_factor()

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["factor"].widget.attrs["placeholder"] = ""
