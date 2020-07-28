"""Admin pages for schemes models.

On default generates list view admins for all models
"""
from django.contrib.admin import StackedInline, register

from espressodb.base.admin import register_admins
from espressodb.base.admin import ListViewAdmin as LVA

from strops.schemes.models import (
    ExpansionScheme,
    ExpansionParameter,
    ExpansionOrder,
    OperatorRelation,
)


class ExpansionParameterInline(StackedInline):
    model = ExpansionParameter
    extra = 1


@register(ExpansionScheme)
class ExpansionSchemeAdmin(LVA):
    inlines = (ExpansionParameterInline,)


class ExpansionOrderInline(StackedInline):
    model = ExpansionOrder
    extra = 1


register_admins(
    "strops.schemes",
    exclude_models=["ExpansionScheme", "OperatorRelation", "ExpansionOrder"],
)


@register(OperatorRelation)
class OperatorRelationAdmin(LVA):
    inlines = (ExpansionOrderInline,)
    autocomplete_fields = ("source", "target")
