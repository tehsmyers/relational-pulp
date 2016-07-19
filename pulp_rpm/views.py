from pulp.views import ContentUnitViewSet, router
from pulp_rpm import models, serializers


# TODO: Magic trick: autogenerate viewsets by finding contentunit model classes
class RPMViewSet(ContentUnitViewSet):
    queryset = models.RPM.objects.all()
    serializer_class = serializers.RPMSerializer


class SRPMViewSet(ContentUnitViewSet):
    """This is a test!

    Check out the SRPM API endpoint to see it render this docstring.
    """
    queryset = models.SRPM.objects.all()
    serializer_class = serializers.SRPMSerializer

router.register(r'content/rpm', RPMViewSet)
router.register(r'content/srpm', SRPMViewSet)
