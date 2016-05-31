import uuid
from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Repository(UUIDModel):
    repo_id = models.CharField(max_length=255)

    def __str__(self):
        return self.repo_id

    def __repr__(self):
        return '<{} "{}">'.format(type(self).__name__, str(self))


class ContentUnitQuerySet(models.QuerySet):
    # a normal django queryset, but looks adds the 'cast' method
    # to the DSL, which runs the cast method on the current queryset
    def cast(self):
        # We'd normally want this to be a generator expression, but
        # for demoing purposes it's easier to just realize this as a list
        return [instance.cast for instance in self]

# Make a Manager based on the cast-aware queryset
ContentUnitManager = models.Manager.from_queryset(ContentUnitQuerySet)


# ContentUnit is the "master" model for all content units, and tracks
# the content unit repository relationships as well as the content unit
# type, which is derived from its implementing subclass.
class ContentUnit(UUIDModel):
    repositories = models.ManyToManyField(Repository, related_name='units',
                                          through='_RepositoryContentUnit')
    content_type = models.CharField(max_length=15)

    # Not all content units have files, but if most content units *cough*rpm*cough*
    # have files, this is a good example of the sort of field worth storing in the
    # content unit master table.
    filename = models.FileField(null=True)

    # Tell the default manager to use the cast-aware ContentUnitQuerySet
    objects = ContentUnitManager()

    def save(self, *args, **kwargs):
        # instances of "detail" models that subclass ContentUnit are exposed
        # on instances of ContentUnit by a lowercase version of their model
        # name. That name is what I'm using here to determine the value of
        # content_type. For example, the RPM ContentUnit's attribute is exposed
        # on ContentUnit as the 'rpm' attr, and can be found by inspecting the
        # related name of the implicit OneToOneField created by the ContentUnit
        # subclass. Storing content_type directly on the ContentUnit next to
        # the repository relationship makes it trivial to filter for content
        # units of a specific type or types in one or many repositories.

        # Creating a type-less content unit is disallowed.
        if type(self)._meta.model_name == ContentUnit._meta.model_name:
            raise Exception('Do not instantiate ContentUnit directly.')

        self.content_type = type(self)._meta.model_name
        return super(ContentUnit, self).save(*args, **kwargs)

        # If we do want to disallow this with a better exception, then this is
        # another options:
        # self.content_type = self._meta.model_name:
        # if self.content_type == ContentUnit._meta.model_name:
        #     explode()

    def cast(self):
        return getattr(self, self.content_type)

    @property
    def content_unit(self):
        # This field name is hardcoded, but should be derived by inspecting the
        # unit instance to get the name of the contentunit one-to-one reverse
        # relation
        try:
            return self.contentunit_ptr
        except AttributeError:
            # No content unit pointer means we're already a ContentUnit
            return self

    def __str__(self):
        try:
            obj_str = str(self.cast())
        except AttributeError:
            obj_str = '(foreign type) pk {}'.format(self.pk)
        return "{}: {}".format(self.content_type, obj_str)

    def __repr__(self):
        return '<{} "{}">'.format(type(self).__name__, str(self))


# A "private" model representing the join table between repos and content units
# It's private because it provides information only useful to pulp internals,
# specifically created and updated timestamps for this relationship, which
# is occasionally used by plugins to make the right decision when enforcing
# type-specific constaings (e.g. if you want to check for duplicate NEVRA
# after syncing a yum repo, the updated timestamp tells you which one *not*
# to delete). This model should *never* have to be instantiated directly.
class _RepositoryContentUnit(models.Model):
    repository = models.ForeignKey('Repository', on_delete=models.CASCADE)
    content_unit = models.ForeignKey('ContentUnit', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Normally, using a through model would disable the ability to use
        # handy ManyToMany manager methods, such as add/create/set. Because
        # the fields on our through model are automatically set, we can restore
        # this functionality by telling Django to treat this as an automatically
        # created ManyToMany join table. Adding fields that are not automatically
        # set would break the crap out of this, so don't do that.
        auto_created = True
