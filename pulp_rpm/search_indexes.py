from haystack import indexes
from pulp.search_indexes import ContentUnitIndex
from pulp_rpm.models import RPM, SRPM


class NEVRAUnitIndexBase(ContentUnitIndex):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')
    epoch = indexes.CharField(model_attr='epoch')
    version = indexes.CharField(model_attr='version')
    release = indexes.CharField(model_attr='release')
    arch = indexes.CharField(model_attr='arch')

    def prepare_text(self, obj):
        return str(obj)

    def index_queryset(self, using=None):
        return self.get_model().objects.get_queryset()


class RPMUnitIndex(NEVRAUnitIndexBase, indexes.Indexable):
    def get_model(self):
        return RPM


class SRPMUnitIndex(NEVRAUnitIndexBase, indexes.Indexable):
    def get_model(self):
        return SRPM
