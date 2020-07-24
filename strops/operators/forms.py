"""Forms for the operators app."""
from django import forms

from sympy import sympify
from strops.operators.models import Operator
from strops.utils.fields import FACTOR_VALIDATORS


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
