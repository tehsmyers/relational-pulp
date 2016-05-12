from haystack import indexes


# generic searchindex for all content units, extend this for specific units
class ContentUnitIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True)
    content_type = indexes.CharField(model_attr='content_type')
    repositories = indexes.MultiValueField(faceted=True)

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.get_queryset()

    def prepare_text(self, obj):
        return str(obj)

    def prepare_repositories(self, obj):
        return [repo.repo_id for repo in obj.repositories.all()]
