from rest_framework import serializers

from pulp import models

# XXX: Another entry point. This mapping matches up models with their API serializers
# so that, for example, the ContentUnit serializer knows how cast ContentUnits as
# their specific type.
serializer_registry = {}


class ContentUnitRelatedField(serializers.HyperlinkedRelatedField):
    def to_representation(self, value):
        try:
            serializer = serializer_registry[type(value.cast())]
            return serializer(instance=value).data
        except KeyError:
            # model not in serializer mapping, asplode with a better error
            # once we write one :)
            raise

    class Meta:
        model = models.ContentUnit


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    units = ContentUnitRelatedField(
        view_name='contentunit-detail',
        read_only=True,
        many=True,
    )

    _href = serializers.HyperlinkedIdentityField(
        view_name='repository-detail',
        lookup_field='repo_id',
    )

    class Meta:
        model = models.Repository


class ContentUnitSerializer(serializers.HyperlinkedModelSerializer):
    repositories = serializers.HyperlinkedRelatedField(
        view_name='repository-detail',
        lookup_field='repo_id',
        read_only=True,
        many=True,
    )

    class Meta:
        model = models.ContentUnit


serializer_registry[models.Repository] = RepositorySerializer

# XXX more crappy simulation of entry points
import pulp_rpm.serializers  # NOQA
