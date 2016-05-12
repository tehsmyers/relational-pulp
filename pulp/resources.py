from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS

from pulp.models import ContentUnit, Repository


class ContentUnitResource(ModelResource):
    class Meta:
        queryset = ContentUnit.objects.all()
        resource_name = 'content'
        authorization = Authorization()
        filtering = {
            'repositories': ALL_WITH_RELATIONS,
        }


class RepositoryResource(ModelResource):
    units = fields.ToManyField(
        ContentUnitResource, attribute='units', related_name='repositories', full=True)

    class Meta:
        resource_name = 'repositories'
        include_resource_uri = False
        queryset = Repository.objects.all()
