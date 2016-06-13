from django.core.exceptions import ValidationError
from django.db import models


class ChecksumTypeCharField(models.CharField):
    def to_python(self, value):
        # Should call out to pulp.server.util.sanitize_checksum_type
        # and return the corrected value. For now...
        try:
            return str(value)
        except:  # Some exception that sanitize raises?
            raise ValidationError
