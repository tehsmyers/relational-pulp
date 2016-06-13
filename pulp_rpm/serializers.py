from pulp.serializers import ContentUnitSerializer
from pulp_rpm import models


class RPMSerializer(ContentUnitSerializer):
    class Meta(ContentUnitSerializer.Meta):
        model = models.RPM


class SRPMSerializer(ContentUnitSerializer):
    class Meta(ContentUnitSerializer.Meta):
        model = models.SRPM
