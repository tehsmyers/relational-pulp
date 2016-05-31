from pulp import models, serializers

from rest_framework import routers, viewsets


class RepositoryViewSet(viewsets.ModelViewSet):
    lookup_field = 'repo_id'
    queryset = models.Repository.objects.all()
    serializer_class = serializers.RepositorySerializer


class ContentUnitViewSet(viewsets.ModelViewSet):
    queryset = models.ContentUnit.objects.all()
    serializer_class = serializers.ContentUnitSerializer

router = routers.DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
router.register(r'content', ContentUnitViewSet)
