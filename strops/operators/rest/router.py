"""Links operator view sets to urls."""
from rest_framework import routers

from strops.operators.rest.serializers import OperatorViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r"operators", OperatorViewSet)
