from pulp.serializers import ContentUnitSerializer, serializer_registry
from pulp_rpm import models


class RPMSerializer(ContentUnitSerializer):
    class Meta(ContentUnitSerializer.Meta):
        model = models.RPM


class SRPMSerializer(ContentUnitSerializer):
    class Meta(ContentUnitSerializer.Meta):
        model = models.SRPM

serializer_registry[models.RPM] = RPMSerializer
serializer_registry[models.SRPM] = SRPMSerializer
