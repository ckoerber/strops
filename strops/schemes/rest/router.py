"""Links operator view sets to urls."""
from rest_framework import routers

from strops.schemes.rest.serializers import ExpansionSchemeViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r"schemes", ExpansionSchemeViewSet)
