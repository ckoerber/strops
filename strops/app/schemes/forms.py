"""Forms for the schemes app."""
from django import forms

from strops.app.operators.models import SCALES


class ScaleForm(forms.Form):
    """Form which querries the user about scales."""

    scale = forms.ChoiceField(help_text="What is the physical scale?", choices=SCALES)


class BranchFormSet:
    pass


class OperatorFormSet:
    pass
