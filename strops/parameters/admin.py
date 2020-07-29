"""Admin pages for parameters models.

On default generates list view admins for all models
"""
from django.contrib.admin import StackedInline, register

from espressodb.base.admin import register_admins
from espressodb.base.admin import ListViewAdmin as LVA

from strops.parameters.models import Parameter, ParameterValue


class ParameterValueInline(StackedInline):  # noqa
    model = ParameterValue
    extra = 1


@register(Parameter)
class ParameterAdmin(LVA):  # noqa
    inlines = (ParameterValueInline,)


register_admins("strops.parameters", exclude_models=["Parameter"])
