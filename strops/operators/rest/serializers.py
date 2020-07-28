"""Rest API serializers for operators."""
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.viewsets import ReadOnlyModelViewSet

from strops.utils.tex import latex
from strops.operators.models import Operator


class OperatorSerializer(ModelSerializer):
    """Serializer of operators."""

    expression = CharField(read_only=True)
    latex = CharField(read_only=True)

    def get_expression(self, obj):
        return str(obj.expression)

    def get_latex(self, obj):
        return latex(obj.expression, wrapped=("$", "$"))

    class Meta:
        model = Operator
        fields = [
            "name",
            "expression",
            "lorentz",
            "scale",
            "charge",
            "parity",
            "time",
            "details",
            "latex",
        ]


class OperatorViewSet(ReadOnlyModelViewSet):  # pylint: disable=R0901
    """Serializer view for all operators."""

    queryset = Operator.objects.all()
    serializer_class = OperatorSerializer
