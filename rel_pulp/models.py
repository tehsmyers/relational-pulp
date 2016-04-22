from django.db import models


class Repository(models.Model):
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
        return [instance.cast() for instance in self]

# Make a Manager based on the cast-aware queryset
ContentUnitManager = models.Manager.from_queryset(ContentUnitQuerySet)


# ContentUnit is the "master" model for all content units, and tracks
# the content unit repository relationships as well as the content unit
# type, which is derived from its implementing subclass.
class ContentUnit(models.Model):
    repositories = models.ManyToManyField(Repository, related_name='units')
    content_type = models.CharField(max_length=15)

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

        # If this explodes because of AttributeError on contentunit_ptr,
        # That means you just tried to create a ContentUnit directly, not
        # through a subclass. This should be disallowed. For now, it just
        # explodes. Don't do it. :)
        self.content_type = type(self).contentunit_ptr.field.remote_field.name
        super(ContentUnit, self).save(*args, **kwargs)

    def cast(self):
        return getattr(self, self.content_type)

    def generic_unit(self):
        # This field name is hardcoded, but should be derived by inspecting the
        # unit instance to get the name of the contentunit one-to-one reverse
        # relation
        return getattr(self, 'contentunit_ptr')

    def __str__(self):
        try:
            obj = self.cast()
            obj_str = str(obj)
        except AttributeError:
            obj_str = '(foreign type) pk {}'.format(self.pk)
        return "{}: {}".format(self.content_type, obj_str)

    def __repr__(self):
        return '<{} "{}">'.format(type(self).__name__, str(self))


class NEVRAPackage(ContentUnit):
    KEY_FIELDS = ('name', 'epoch', 'version', 'release', 'arch')

    name = models.CharField(max_length=63)
    epoch = models.CharField(max_length=63)
    version = models.CharField(max_length=63)
    release = models.CharField(max_length=63)
    arch = models.CharField(max_length=63)
    checksum = models.CharField(max_length=63)
    checksumtype = models.CharField(max_length=63)

    class Meta:
        # don't make a table for this, we just want the fields
        abstract = True

    def __str__(self):
        field_values = [getattr(self, field) for field in self.KEY_FIELDS]
        return '-'.join(field_values)

class RPM(NEVRAPackage):
    _content_type_id = 'rpm'


class SRPM(NEVRAPackage):
    _content_type_id = 'srpm'
