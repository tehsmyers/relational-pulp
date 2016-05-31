from __future__ import unicode_literals

from django.apps import AppConfig


class PulpRpmConfig(AppConfig):
    name = 'pulp_rpm'

    def ready(self):
        # Import view here to register them with the content router
        from pulp_rpm import views  # NOQA
