"""Rest API serializers for operators."""
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.viewsets import ReadOnlyModelViewSet

from strops.utils.tex import latex
from strops.operators.models import Operator


class OperatorSerializer(ModelSerializer):
    """Serializer of operators."""

    expression_string = SerializerMethodField("get_expression_string")
    expression_latex = SerializerMethodField("get_expression_latex")
    # type = SerializerMethodField("get_type")
    n_fields = SerializerMethodField("get_n_fields")

    def get_expression_string(self, obj):
        return str(obj.expression)

    def get_expression_latex(self, obj):
        return latex(obj.expression, wrapped=None)

    def get_type(self, obj):
        return obj.specialization.__class__.__name__

    def get_n_fields(self, obj):
        return len(
            [f for f in obj.specialization.get_open_fields() if "field" in f.name]
        )

    class Meta:
        model = Operator
        fields = [
            "id",
            "name",
            "n_fields",
            "expression_string",
            "scale",
            "details",
            "expression_latex",
        ]


class OperatorViewSet(ReadOnlyModelViewSet):  # pylint: disable=R0901
    """Serializer view for all operators."""

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
