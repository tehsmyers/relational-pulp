from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from pulp.fields import ChecksumTypeCharField
from pulp.models import (UUIDModel, Slugged, Repository, ContentUnit,
                         NamedTupleDescriptor, GenericModel, GenericKeyValueStore)


class RPMRepositoryProxy(Repository):
    # Looks like a typed repository, but is just a django proxy model that can be used by
    # yum-specific models as ForeignKey targets without adding a bunch of reverse relations
    # to generic Repository instances. This distinction only exists in software; anything
    # related to this proxy is, at the DB level, still related to Repository
    class Meta:
        proxy = True


class Errata(UUIDModel, Slugged):
    # slug (formerly errata_id) should be the "id" field in updateinfo.xml
    repository = models.ForeignKey(RPMRepositoryProxy, related_name='errata')

    # XXX These are StringFields in mongo, but are obviously datetime stamps
    issued = models.DateTimeField()
    updated = models.DateTimeField()
    description = models.TextField()
    solution = models.TextField()
    summary = models.TextField()
    # XXX This is a StringField in mongo, but should probably always be a positive int?
    pushcount = models.PositiveIntegerField()
    reboot_suggested = models.BooleanField(default=False)
    errata_from = models.CharField(max_length=255)
    severity = models.CharField(max_length=255)
    rights = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    release = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)


class ErrataReferenceAttributes(GenericKeyValueStore):
    # Used by ErrataReference to store XML attributes that are
    # specific to different errata reference types
    pass


class ErrataReference(GenericKeyValueStore):
    # The possible attrs on errata references might be well-defined, in which case we should
    # model it out. Looking at a RHEL errata, all references have an href and a type, which
    # are modeled here, with the rest of the attrs living in a generic key value store.
    errata = models.ForeignKey(Errata, related_name='references')
    href = models.TextField()
    type = models.CharField(max_length=63)
    attrs = GenericRelation(ErrataReferenceAttributes)


class ErrataCollection(UUIDModel):
    errata = models.ForeignKey(Errata, related_name='pkglist')
    # short acts as collection id, but to keep this consistent with the updateinfo XML,
    # it makes sense to just call this short and leave a comment here about how it's used
    short = models.CharField(max_length=255)
    name = models.CharField(max_length=255)


class ErrataPackage(UUIDModel):
    collection = models.ForeignKey(ErrataCollection, related_name='packages')
    name = models.CharField(max_length=255)
    epoch = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    release = models.CharField(max_length=255)
    arch = models.CharField(max_length=255)
    src = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)

    # It might be worth having a generic Checksum model if we've got a lot of models with these
    # fields.  # For now, these are explicitly defined here with names based on updateinfo.xml
    sum = models.CharField(max_length=255)
    sum_type = models.CharField(max_length=255)


# XXX Something that knows the comps stuff we should definitely double check this.
# I'm not 100% sure that I brought all the right fields over.
class CompsPackageReq(GenericModel):
    # model for all the packagereq elements in a comps pkglist
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=63)


# CompsGroupId and CompsOptionGroupId could potentially be the same model if we added an "optional"
# boolean, but it's probably easier to put them in separate tables and be explicit about it. A lot
# of common fields across these different types mean there are opportunities to DRY things up.
class CompsGroupID(GenericModel):
    # for groupid elements in grouplists - seen in group, category, and environment
    name = models.CharField(max_length=255)


class CompsOptionGroupID(GenericModel):
    # for groupid elements in optionlists - seen in group, environment, possible category
    name = models.CharField(max_length=255)


class CompsTranslatedName(GenericModel):
    # for storing name with "xml:lang" attrs - seen in group, category, and environment
    lang = models.CharField(max_length=63)
    value = models.CharField(max_length=255)


class CompsTranslatedDescription(GenericModel):
    # for storing description with "xml:lang" attrs - seen in group, category, and environment
    lang = models.CharField(max_length=63)
    value = models.CharField(max_length=255)


class Comps(UUIDModel):
    # stash all the top-level comps attrs on a single object so that
    # the interface lines up with the actual comps structure
    repository = models.OneToOneField(RPMRepositoryProxy, related_name='comps')


class CompsGroup(UUIDModel, Slugged):
    # slug should be the 'id' XML tag value for this group element
    parent = models.ForeignKey(Comps, related_name='groups')

    name = models.CharField(max_length=255)
    packagelist = GenericRelation(CompsPackageReq)
    description = models.TextField()
    basearchonly = models.NullBooleanField(default=None)
    default = models.BooleanField(default=False)
    display_order = models.IntegerField()
    user_visible = models.BooleanField(default=False)
    # these translated_ fields are a bit of a hack to deal with some XML metadata
    # that is used to mark the language translated fields
    translated_name = GenericRelation(CompsTranslatedName)
    translated_description = GenericRelation(CompsTranslatedDescription)
    langonly = models.CharField(max_length=63)


class CompsCategory(UUIDModel, Slugged):
    # slug should be the 'id' XML tag value for this category element
    parent = models.ForeignKey(Comps, related_name='categories')

    name = models.CharField(max_length=255)
    description = models.TextField()
    display_order = models.IntegerField()
    translated_name = GenericRelation(CompsTranslatedName)
    translated_description = GenericRelation(CompsTranslatedDescription)
    grouplist = GenericRelation(CompsGroupID)


class CompsEnvironment(UUIDModel, Slugged):
    # slug should be the 'id' XML tag value for this environment element
    parent = models.ForeignKey(Comps, related_name='environments')

    name = models.CharField(max_length=255)
    grouplist = GenericRelation(CompsGroupID)
    optionlist = GenericRelation(CompsOptionGroupID)
    description = models.TextField()
    display_order = models.IntegerField()
    translated_name = GenericRelation(CompsTranslatedName)
    translated_description = GenericRelation(CompsTranslatedDescription)


class CompsLangpacks(UUIDModel, Slugged):
    # slug should be the 'id' XML tag value for this langpacks element
    parent = models.ForeignKey(Comps, related_name='langpacks')


class CompsLangpacksMatch(UUIDModel):
    # match element in a langpacks entry
    langpack = models.ForeignKey(CompsLangpacks, related_name='matches')
    name = models.CharField(max_length=255)
    install = models.CharField(max_length=255)


class Distribution(ContentUnit, Slugged):
    # The pulp 2 model for this has a pretty big disclaimer about how the Distribution model
    # should be rewritten. This doesn't attempt that at all, instead it just brings
    # Distribution over as a normal ContentUnit with the same fields. Note that the "files"
    # field is missing now that all ContentUnit instance can relate to zero or more files.
    # slug field is 'distribution_id' in Mongo, weakly indicating that it might not actually
    # be a content unit from a data modeling perspective.
    # Also, all of these lengths are probably ridiculous.
    family = models.CharField(max_length=255)
    variant = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255)
    arch = models.CharField(max_length=255)

    # I hope we're just storing this and not doing anything with it? Otherwise, DateTimeField...
    timestamp = models.FloatField()
    packagedir = models.CharField(max_length=255)


class ISO(ContentUnit):
    # XXX This whole model is likely to go away in favor of platform support
    # for generic file syncing, so I'm not too interested to dig to deep, like
    # looking into how checksum(s) should be related to ISO. This model had
    # a "size" field and a "checksum" field, which presumably can be handled by
    # the built-in relationship to ContentUnitFile.
    name = models.CharField(max_length=255)


class YumMetadataFile(ContentUnit):
    # A file entry in repomd.
    # XXX Do we store files with this? If not, can just be a UUIDModel subclass,
    # and FK back to Repository, and either track checksums right on this model
    # or through the Checksum generic relation. For now, this is a ContentUnit,
    # related to ContentUnitFiles, which have checksum fields.
    data_type = models.CharField(max_length=255)


class PackageBase(ContentUnit):
    # Formerly "NonMetadataPackage", a base class for all things that are "not metadata".
    # In Pulp 2's RPM plugin, many objects that are repository metadata are modeled as
    # ContentUnits. For Pulp 3, these have been converted to a normal model base, and FK
    # back to the repository that owns them. All DRPMS, SRPMS, and RPMS inherit from this.
    version = models.CharField(max_length=63)
    release = models.CharField(max_length=63)

    # We already have a model for checksums; this specifically represents the checksum provided
    # by the source repo, which should be included in a yum unit's key fields to account, e.g.
    # for different RPMs with the same NEVRA. I might hate this, but don't understand yum repo
    # metadata enough at the moment to come up with a better solution for unit key uniqueness.
    checksum = models.CharField(max_length=255)
    checksumtype = ChecksumTypeCharField(max_length=63)

    # We generate these two for sorting, but we could possibly
    # store the sortable value for each of these in the "normal"
    # DB field using a special Django field that converts them
    # back and forth. For now, they're being left blank, but we'll
    # need a way to update these when a package version is added or
    # changed. I'd love to see them go away, since there are other
    # ways we can do this without custom fields or storing duplicate
    # data, like annotation or better modeling of the data
    version_sort_index = models.CharField(max_length=63)
    release_sort_index = models.CharField(max_length=63)

    class Meta:
        abstract = True


class DRPM(PackageBase):
    pass


class RPMBase(PackageBase):
    # More specific version of PackageBase for SRPM and RPM types
    NEVRA_FIELDS = ('name', 'epoch', 'version', 'release', 'arch')
    KEY_FIELDS = NEVRA_FIELDS + ('checksum', 'checksumtype')

    name = models.CharField(max_length=127)
    epoch = models.CharField(max_length=63)
    arch = models.CharField(max_length=63)

    NEVRA_TUPLE = NamedTupleDescriptor('NEVRA_FIELDS', 'NevraTuple')

    @property
    def nevra_tuple(self):
        values = (getattr(self, field) for field in self.NEVRA_FIELDS)
        return self.NEVRA_TUPLE._make(values)

    class Meta:
        abstract = True


class RPM(RPMBase):
    pass


class SRPM(RPMBase):
    pass
