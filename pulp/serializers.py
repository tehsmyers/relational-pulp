from rest_framework import serializers

from pulp import models

# XXX: Another entry point. This mapping matches up models with their API serializers
# so that, for example, the ContentUnit serializer knows how cast ContentUnits as
# their specific type.
serializer_registry = {}


class ContentUnitRelatedField(serializers.HyperlinkedRelatedField):
    """ContentUnit Hyperlinked Related API field that knows to cast unit URLs"""
    def get_object(self, *args, **kwargs):
        # return the cast object, not the generic contentunit
        return super(ContentUnitRelatedField, self).get_object(*args, **kwargs).cast()

    def get_url(self, obj, view_name, *args, **kwargs):
        # return the url to the cast unit, not the generic unit
        view_name = '{}-detail'.format(obj.cast()._meta.model_name)
        return super(ContentUnitRelatedField, self).get_url(obj.cast(), view_name, *args, **kwargs)

    class Meta:
        model = models.ContentUnit


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    _href = serializers.HyperlinkedIdentityField(
        view_name='repository-detail',
        lookup_field='repo_id',
    )

    content_unit_counts = serializers.DictField()

    class Meta:
        model = models.Repository
        fields = ('_href', 'content_unit_counts', 'repo_id', 'display_name',
                  'description', 'last_unit_added', 'last_unit_removed')


class ContentUnitSerializer(serializers.HyperlinkedModelSerializer):
    repositories = serializers.HyperlinkedRelatedField(
        view_name='repository-detail',
        lookup_field='repo_id',
        read_only=True,
        many=True,
    )

    class Meta:
        model = models.ContentUnit
