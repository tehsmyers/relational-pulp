import importlib

from django.apps import AppConfig, apps


class PulpConfig(AppConfig):
    name = 'pulp'

    def ready(self):
        # views importer to register viewsets with the api
        # XXX: this should be done in a more explicit way,
        # not relying on app names
        for app in apps.get_app_configs():
            if app.name.startswith('pulp_'):
                views_module = '{}.views'.format(app.name)
                importlib.import_module(views_module)
