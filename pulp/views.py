from pulp import models, serializers

from rest_framework import routers, viewsets


class RepositoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = models.Repository.objects.all()
    serializer_class = serializers.RepositorySerializer


# XXX DO NOT register ContentUnitViewSet with the router.
# It's here to be subclasses by the specific unit types,
# not to provide its own views. *Always* drive unit API
# views to the specific type.
class ContentUnitViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContentUnitSerializer

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
