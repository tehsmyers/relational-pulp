from pulp.views import ContentUnitViewSet, router
from pulp_rpm import models, serializers


class RPMViewSet(ContentUnitViewSet):
    queryset = models.RPM.objects.all()
    serializer_class = serializers.RPMSerializer


class SRPMViewSet(ContentUnitViewSet):
    queryset = models.SRPM.objects.all()
    serializer_class = serializers.SRPMSerializer

router.register(r'content/rpm', RPMViewSet)
router.register(r'content/srpm', SRPMViewSet)
