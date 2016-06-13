from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

from pulp.fields import ChecksumTypeCharField
from pulp.models import ContentUnit, GenericModel, Repository, UUIDModel


class YumRepository(Repository):
    # Looks like a typed repository, but is just a django proxy model that can be used by
    # yum-specific models as ForeignKey targets without adding a bunch of reverse relations
    # to generic Repository instances.
    class Meta:
        proxy = True


class Errata(UUIDModel):
    errata_id = models.CharField(max_length=255)
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


class ErrataReference(UUIDModel):
    errata = models.ForeignKey(Errata, related_name='references')
    href = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=63)
    id = models.CharField(max_length=63)


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
    # renamed sum to digest to avoid conflicting with builtin 'sum' and to match checksum model
    digest = models.CharField(max_length=255)


# XXX Something that knows the comps stuff we should definitely double check this.
# I'm not 100% sure that I brought all the right fields over.
class CompsPackageReq(GenericModel):
    # model for all the packagereq elements in a comps pkglist
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=63)


class CompsGroupID(GenericModel):
    # for groupid elements in grouplists
    name = models.CharField(max_length=255)


class CompsOptionGroupID(GenericModel):
    # for groupid elements in optionlists
    name = models.CharField(max_length=255)


class CompsTranslatedName(GenericModel):
    # for storing name fields with "xml:lang" attrs
    lang = models.CharField(max_length=63)
    value = models.CharField(max_length=255)


class CompsTranslatedDescription(GenericModel):
    # for storing description fields with "xml:lang" attrs
    lang = models.CharField(max_length=63)
    value = models.CharField(max_length=255)


class CompsLangpacksMatch(GenericModel):
    # match element in a langpacks entry
    name = models.CharField(max_length=255)
    install = models.CharField(max_length=255)


# XXX We could potentially relate all of these Comps children to a Comps container type,
# but for now they all just relate straight back to a YumRepository, just like they do
# in pulp 2.
class CompsGroup(UUIDModel):
    repository = models.ForeignKey(YumRepository)
    group_id = models.CharField(max_length=255)

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


class CompsCategory(UUIDModel):
    repository = models.ForeignKey(YumRepository)
    category_id = models.CharField(max_length=255)

    name = models.CharField(max_length=255)
    description = models.TextField()
    display_order = models.IntegerField()
    translated_name = GenericRelation(CompsTranslatedName)
    translated_description = GenericRelation(CompsTranslatedDescription)
    grouplist = GenericRelation(CompsGroupID)


class CompsEnvironment(UUIDModel):
    repository = models.ForeignKey(YumRepository)
    environment_id = models.CharField(max_length=255)

    name = models.CharField(max_length=255)
    grouplist = GenericRelation(CompsGroupID)
    optionlist = GenericRelation(CompsOptionGroupID)
    description = models.TextField()
    display_order = models.IntegerField()
    translated_name = GenericRelation(CompsTranslatedName)
    translated_description = GenericRelation(CompsTranslatedDescription)


class CompsLangpacks(UUIDModel):
    repository = models.ForeignKey(YumRepository)
    matches = GenericRelation(CompsLangpacksMatch)


class Distribution(ContentUnit):
    # The pulp 2 model for this has a pretty ig disclaimer about how the Distribution model
    # should be rewritten. This doesn't attempt that at all, instead it just brings
    # Distribution over as a normal ContentUnit with the same fields. Note that the "files"
    # field is missing now that all ContentUnit instance can relate to zero or more files.
    # Also, all of these lengths are probably ridiculous.
    distribution_id = models.CharField(max_length=255)
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
    # related to ContentUnitFiles.
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

    class Meta:
        abstract = True


class RPM(RPMBase):
    pass


class SRPM(RPMBase):
    pass
