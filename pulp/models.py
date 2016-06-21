import hashlib
import uuid
from hashlib import sha256
from collections import namedtuple

from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import signals
from django.utils import timezone

from pulp.storage import content_unit_path

Checksum = namedtuple('Checksum', ('algorithm', 'digest'))


class UUIDModel(models.Model):
    # plain old django model, with a UUID PK.
    # postgres has native support for UUIDs which makes this non-criminal behavior,
    # and allows us to keep, for example, mongo unit _id values when migrating
    # from mongo to postgres so that pulp users with references to those units by
    # ID don't have those references broken.
    # https://www.postgresql.org/docs/current/static/datatype-uuid.html
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # ...we have zero interest in using a mongo-specific datatype (ObjectId) as
    # the django PK.

    class Meta:
        abstract = True


class GenericModel(models.Model):
    # abstract base that can be added to a model to provide the required fields for generic
    # relations. Must mixed in with UUIDModel base.
    # https://docs.djangoproject.com/en/1.8/ref/contrib/contenttypes/#generic-relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class GenericKeyValueStore(UUIDModel, GenericModel):
    key = models.CharField(max_length=255)
    # we need to make this a TextField, and leave migrating its contents to implementers.
    # That's easy enough when the implementer is pulp itself, but care should be taken to
    # do as little as possible with these during migration so data isn't lost.
    value = models.TextField()

    class Meta:
        abstract = True


class Config(GenericKeyValueStore):
    # Used by pulp and users to store k/v config data on a model
    pass


class Notes(GenericKeyValueStore):
    # Used by users to store arbitrary k/v data on a model
    pass


class Scratchpad(GenericKeyValueStore):
    # Used by pulp internals to store arbitrary k/v data on a model
    # e.g. Used by plugins to store type-specific repo data in lieu
    # of having typed repos.
    pass


class Repository(UUIDModel):
    repo_id = models.CharField(max_length=255, db_index=True, unique=True)
    display_name = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')

    units = models.ManyToManyField('ContentUnit', related_name='repositories',
                                   through='RepositoryContentUnit')

    notes = GenericRelation(Notes)
    scratchpad = GenericRelation(Scratchpad)

    # these get populated by signals attached to the units relation
    last_unit_added = models.DateTimeField(blank=True, null=True)
    last_unit_removed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.repo_id

    def __repr__(self):
        return '<{} "{}">'.format(type(self).__name__, str(self))

    # Normally you'd just repo.units.add/.remove, but Django disables this when using
    # a through model, so these are here to help making units a little easier.
    def add_units(self, *units):
        for unit in units:
            RepositoryContentUnit.objects.get_or_create(repository=self, content_unit=unit)

    def remove_units(self, *units):
        RepositoryContentUnit.objects.filter(repository=self, content_unit__in=units).delete()

    @property
    def content_unit_counts(self):
        # This was a field in mongo, but through annotation can be derived by postgres
        unit_counts = self.units.values('content_type').annotate(
            count=models.Count('content_type'))
        return {c['content_type']: c['count'] for c in unit_counts}

    @classmethod
    def from_repository(cls, repository):
        # Useless in this class, but handy for proxy subclasses,
        # e.g. PluginRepositoryProxy.from_repository(repository)
        return cls.objects.get(pk=repository.pk)


class Importer(UUIDModel):
    repository = models.ForeignKey(Repository, related_name='importers')
    importer_type_id = models.CharField(max_length=255)
    config = GenericRelation(Config)
    scratchpad = GenericRelation(Scratchpad)
    last_sync = models.DateTimeField(blank=True, null=True)


class ContentUnitQuerySet(models.QuerySet):
    # a normal django queryset, but adds the 'cast' method
    # to the DSL, which runs the cast method on the current queryset
    def cast(self):
        return (instance.cast() for instance in self)

# Make a Manager based on the cast-aware queryset
ContentUnitManager = models.Manager.from_queryset(ContentUnitQuerySet)


class _ContentUnitNamedTupleDescriptor:
    """A descriptor used to dynamically generate and cache the namedtuple type for a ContentUnit

    The generated namedtuple is cached, keyed to the class for which it was generated, so
    this property will return the same namedtuple for each class that inherits an instance
    of this descriptor. Furthermore, the namedtuple cache behaves as a singleton, so all instances
    of this descriptor use the same shared cache.

    In the class scope, descriptor __set__ methods are not used by the type metaclass,
    so instances of this class should only be bound to names that LOOK_LIKE_CONSTANTS,
    effectively making this a lazily-evaluated read-only class property.

    """
    _cache = {}

    def __get__(self, obj, cls):
        if cls not in self._cache:
            self._cache[cls] = namedtuple(cls._get_content_type(), cls.KEY_FIELDS)
        return self._cache[cls]


# ContentUnit is the "master" model for all content units, and tracks
# the content unit repository relationships as well as the content unit
# type, which is derived from its implementing subclass.
class ContentUnit(UUIDModel):
    content_type = models.CharField(max_length=15)

    # formerly the pulp_user_metadata field
    notes = GenericRelation(Notes)

    # Tell the default manager to use the cast-aware ContentUnitQuerySet
    objects = ContentUnitManager()

    # stashing this in the db with an index makes it a little faster to check the uniqueness
    # of a unit's key. Unit keys should be unique across all content units in all plugins.
    key_digest = models.CharField(max_length=64, db_index=True, unique=True)

    NAMED_TUPLE = _ContentUnitNamedTupleDescriptor()

    KEY_FIELDS = ['pk']

    # Similar to the related methods on Repository
    def add_repos(self, *repos):
        for repo in repos:
            RepositoryContentUnit.objects.get_or_create(repository=repo, content_unit=self)

    def remove_repos(self, *repos):
        RepositoryContentUnit.objects.filter(repository__in=repos, content_unit=self).delete()

    @property
    def key_tuple(self):
        # All other unit key representations are generated from this property.
        # ContentUnit does not declare KEY_FIELDS, so instances must be cast before accessing this.
        self = self.cast()
        values = (getattr(self, field) for field in self.KEY_FIELDS)
        return self.NAMED_TUPLE._make(values)

    @property
    def key_str(self):
        return '{}'.format('-'.join(str(v) for v in self.key_tuple if v))

    @property
    def key_dict(self):
        # _asdict is an OrderedDict as of python 3.1
        return self.key_tuple._asdict()

    def hash_key(self, algorithm=None):
        _hash = algorithm or sha256()
        for key, value in self.key_dict.items():
            _hash.update('{}{}'.format(key, value).encode('utf8'))
        return _hash.hexdigest()

    # really a derived class property, but we can make that work later if we really want to
    # get rid of the parenthesis when accessing this
    @classmethod
    def _get_content_type(cls):
        return cls._meta.model_name

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
        # XXX Should probably be handled in a pre-save signal
        if not self.content_type:
            self.content_type = self._get_content_type()
            if self.content_type == ContentUnit._meta.model_name:
                raise Exception('Do not save ContentUnit instances directly.')

        # Update the stored key digest representing the unit key
        # XXX Should probably be handled in a pre-save signal
        self.key_digest = self.hash_key()

        # TODO: else clause here that makes sure the content type is known to pulp
        # or some other mechanism to prevent unknown types being saved to the db
        return super(ContentUnit, self).save(*args, **kwargs)

    def cast(self):
        if self._get_content_type() == self.content_type:
            # If the current instance is already cast, return it rather than instantating a new one
            return self
        else:
            try:
                # otherwise, return the cast model attribute for this instance
                return getattr(self, self.content_type)
            except AttributeError:
                # Unknown content type. The generic content type is as specific as
                # we can get here. This is a great place to throw a log message about
                # encountering an unmodelled type.
                return self

    @property
    def content_unit(self):
        if type(self) is ContentUnit:
            return self

        try:
            # This field name is hardcoded, but should be derived by inspecting the
            # unit instance to get the name of the contentunit one-to-one reverse
            # relation
            return self.contentunit_ptr
        except AttributeError:
            # No content unit pointer means we're already a ContentUnit
            return self

    def __repr__(self):
        if isinstance(getattr(self, self.content_type, None), ContentUnit):
            obj_str = self.key_str
            if type(self) is ContentUnit:
                obj_str = '{}: {}'.format(self.content_type, obj_str)
        else:
            # This can happen if types are in the DB that are no longer known,
            # such as if a plugin was uninstalled.
            obj_str = 'unknown type {}, pk {}'.format(self.content_type, self.pk)
        return '<{} "{}">'.format(type(self).__name__, obj_str)

    def __str__(self):
        return self.key_str


class ContentUnitFile(UUIDModel):
    # This model does not exist in pulp 2. It is intended to deal with the fact
    # that some content units are represented by multiple files (For example,
    # Distribution in pulp_rpm) by making all CU -> File relations be to-many.
    # It also incorporates some of the discussion in https://pulp.plan.io/issues/1647
    # to stash the checksum of the unit file along with the file size name
    unit = models.ForeignKey(ContentUnit, related_name='files')
    content = models.FileField(upload_to=content_unit_path, max_length=255)
    downloaded = models.BooleanField(default=False)

    # suggested in 1647, but I'm not sure of the value unless the goal is for a quick
    # integrity check to make sure the stored file on-disk has the size that we think
    # it should with a stat before checksumming to verify. Stat returns bytes, so
    # this stores bytes.
    file_size = models.BigIntegerField()

    # also from 1647, but I'm even less sure of the value, such that I'm only including
    # it as an example of how we might do it. The purpose of the origin field (at the
    # time I'm writing this, at least) isn't well defined, so I'm assuming that it'll
    # be a string of unknown max length, e.g. TextField.
    # origin = models.TextField()

    # hash fields
    # our hash support is entirely dependent (right now, at least) on what hashlib
    # supports, so these fields are based on values in hashlib.algorithms_guaranteed,
    # with max_length based on the hexdigest length of hashes generated by those algos
    md5 = models.CharField(max_length=32, blank=True, null=True)
    sha1 = models.CharField(max_length=40, blank=True, null=True)
    sha256 = models.CharField(max_length=64, blank=True, null=True)
    sha512 = models.CharField(max_length=128, blank=True, null=True)

    @property
    def digests(self):
        # An example interface to get at the digest fields in one place
        return dict(self._digest_generator())

    @property
    def best_checksum(self):
        # "best" is subjective, so this is another example interface for how we might use
        # the hash fields in a more generic way, in this case by returning on the "best"
        # hash, where "best" is the longest hash, determined by returning the first digest
        # tuple in a list sorted by hash length, descending, or None if there's no digest
        # for this file.

        try:
            return sorted(self._digest_generator(), key=lambda c: len(c.digest), reverse=True)[0]
        except IndexError:
            # No hashes to sort, so the [0] index above exploded
            return None

    def save(self, *args, **kwargs):
        # I'm not sure if we want to calculate all possible checksums on a file when saved, but
        # it's certainly possible to do so. Since the files we get often have checksums associated
        # with them, this seems like the sort of thing we'd want to do as an optional behavior in
        # plugin. It's here as another example of fun things we can do with Django.
        if self.content:
            hashers = {algo: getattr(hashlib, algo)() for algo in self._hash_field_generator()}

            # this is remarkably inefficient! :)
            for line in self.content.readlines():
                for hasher in hashers.values():
                    hasher.update(line.encode('utf8'))

            for algo, hasher in hashers.items():
                setattr(self, algo, hasher.hexdigest())

            self.file_size = self.content.size

        super(ContentUnitFile, self).save(*args, **kwargs)

    def _hash_field_generator(self):
        for field in self._meta.fields:
            if field.name in hashlib.algorithms_guaranteed:
                yield field.name

    def _digest_generator(self):
        # yields Checksum namedtuples for any digest fields that have values
        for field_name in self._hash_field_generator():
            field_value = getattr(self, field_name)
            if field_value:
                yield Checksum(field_name, field_value)

    def __repr__(self):
        return '<{} "{}">'.format(type(self).__name__, self.content.name)


# A through model representing the join table between repos and content units
class RepositoryContentUnit(models.Model):
    # delete this RCU if either the related repo or contentunit are deleted
    repository = models.ForeignKey('Repository', on_delete=models.CASCADE)
    content_unit = models.ForeignKey('ContentUnit', on_delete=models.CASCADE)

    # These stamps are the main reason this model exists explicitly. If we can get rid
    # of the need for these, this entire model can be autogenerated by Django, which
    # makes associating repos and content units easier.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return '<{} "{}: {}">'.format(
            type(self).__name__, self.repository.repo_id, self.content_unit.pk)

    class Meta:
        ordering = ['updated']
        get_latest_by = 'updated'
        unique_together = [('repository', 'content_unit')]


def units_changed(repository, action):
    # update repo last_changed_* timestamps based on the action taken
    # XXX: It seems like this would be pretty slow and not very useful,
    # so figure out what this is for and if we can get rid of it
    now = timezone.now()
    if action == 'save':
        update = {'last_unit_added': now}
    elif action == 'delete':
        update = {'last_unit_removed': now}
    else:
        # unknown action
        return

    for k, v in update.items():
        setattr(repository, k, v)
    repository.save(update_fields=update.keys())


def units_saved(sender, instance, **kwargs):
    units_changed(instance.repository, 'save')


def units_deleted(sender, instance, **kwargs):
    units_changed(instance.repository, 'delete')

signals.pre_save.connect(units_saved, sender=RepositoryContentUnit)
signals.post_delete.connect(units_deleted, sender=RepositoryContentUnit)
