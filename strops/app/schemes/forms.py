"""Forms for the schemes app."""
from django import forms

from strops.app.operators.models import SCALES
from strops.app.schemes.models import ExpansionScheme


class ScaleForm(forms.Form):
    """Form which querries the user about scales."""

    scale = forms.ChoiceField(help_text="What is the physical scale?", choices=SCALES)


class SourceTargetScaleForm(forms.Form):
    """Form which querries the user about source and target scales."""

    source_scale = forms.ChoiceField(
        help_text="What is the source physical scale?", choices=SCALES, disabled=True
    )
    target_scale = forms.ChoiceField(
        help_text="What is the target physical scale?", choices=SCALES
    )


class ExpansionSchemeForm(forms.Form):
    scheme = forms.ModelChoiceField(
        queryset=ExpansionScheme.objects.all(),
        help_text="Which scheme would you like to choose?",
        empty_label=None,
        widget=forms.RadioSelect(),
    )
    source_scale = forms.CharField(widget=forms.HiddenInput(), required=False)
    target_scale = forms.CharField(widget=forms.HiddenInput(), required=False)


class BranchFormSet:
    pass


class OperatorFormSet:
    pass
