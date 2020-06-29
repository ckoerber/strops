"""Admin pages for operators models

On default generates list view admins for all models
"""
from django.contrib.admin import register, TabularInline
from espressodb.base.admin import register_admins, ListViewAdmin

from strops.app.operators.models import Basis, Operator


class LVA(ListViewAdmin):
    display_instance_names = False


class BasisInline(TabularInline):
    model = Basis
    extra = 2


@register(Operator)
class OperatorAdmin(LVA):
    inlines = (BasisInline,)


register_admins("strops.app.operators", exclude_models=["Operator"], admin_class=LVA)
