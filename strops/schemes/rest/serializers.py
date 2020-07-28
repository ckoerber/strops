"""Rest API serializers for expansion schemes."""
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from strops.schemes.models import ExpansionScheme


class ExpansionSchemeSerializer(ModelSerializer):
    """Serializer of expansion schemes."""

    class Meta:
        model = ExpansionScheme
        fields = [
            "name",
            "source_scale",
            "target_scale",
            "description",
            # "references",
        ]


class ExpansionSchemeViewSet(ReadOnlyModelViewSet):  # pylint: disable=R0901
    """Serializer view for all expansion schemes."""

    queryset = ExpansionScheme.objects.all()
    serializer_class = ExpansionSchemeSerializer
