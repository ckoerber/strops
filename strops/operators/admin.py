"""Admin pages for operators models

On default generates list view admins for all models
"""
from django.contrib.admin import register, ModelAdmin
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField

from espressodb.base.admin import register_admins
from espressodb.base.admin import ListViewAdmin as LVA

from strops.operators.models import Operator


class ListViewAdmin(LVA):
    @staticmethod
    def instance_name(obj) -> str:
        """Returns the name of the instance
        Arguments:
            obj: The model instance to render.
        """
        return obj.latex if hasattr(obj, "latex") else str(obj)


@register(Operator)
class OperatorAdmin(ModelAdmin):
    def matrices(self, obj) -> str:
        return obj.matrices

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            matrices=Concat(
                F("twofieldoperator__matrix1"),
                Value(" "),
                F("fourfieldoperator__matrix1"),
                Value(" * "),
                F("fourfieldoperator__matrix2"),
                Value(" * "),
                F("fourfieldoperator__matrix3"),
                output_field=CharField(),
            )
        )

    def visit_sum(self, obj):
        return obj.visit_sum

    search_fields = ("name", "matrices")
    list_display = ("name", "matrices")


register_admins(
    "strops.operators", exclude_models=["Operator"], admin_class=ListViewAdmin
)
