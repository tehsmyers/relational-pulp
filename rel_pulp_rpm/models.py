from __future__ import unicode_literals

from django.db import models

from rel_pulp.models import ContentUnit


class NEVRAPackage(ContentUnit):
    KEY_FIELDS = ('name', 'epoch', 'version', 'release', 'arch', 'checksum', 'checksumtype')

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
