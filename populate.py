import io
import random
from collections import OrderedDict

import coolname
from django.core.files import File
from progress.bar import IncrementalBar as Bar

from pulp import models as platform
from pulp_rpm import models as rpm

# minimum number of things to cram into the db
to_create = OrderedDict()
to_create[platform.Repository] = 10
to_create[rpm.SRPM] = 10
to_create[rpm.RPM] = 100


def populate_repository(model, i):
    repo_name = coolname.generate_slug(2)
    repo, created = platform.Repository.objects.get_or_create(repo_id=repo_name)
    return repo


def create_rpm_or_srpm(model, i):
    name = coolname.generate_slug(2)
    unit, created = model.objects.get_or_create(
        name=name, epoch='epoch', version='version', release='release', arch='arch')
    num_repos_added = int(random.random() * to_create[platform.Repository]) + 1
    repos = platform.Repository.objects.all().order_by('?')[:num_repos_added]
    unit.add_repos(*repos)

    if not unit.files.all():
        filename = '{}.{}'.format(unit, unit.content_type)
        cuf = platform.ContentUnitFile()
        cuf.content = File(io.StringIO(filename), name=filename)
        cuf.unit = unit
        cuf.save()

    return unit


def populate_rpm(model, i):
    return create_rpm_or_srpm(model, i)


def populate_srpm(model, i):
    return create_rpm_or_srpm(model, i)

for model, num_to_create in to_create.items():
    model_name = model._meta.model_name
    bar = Bar('Creating {}'.format(model_name), max=num_to_create)
    model_count = model.objects.count()
    create_f = globals()['populate_{}'.format(model_name)]

    for i in range(num_to_create):
        ident = '{}{}'.format(model_name, i)
        if i < model_count:
            unit = model.objects.all()[i]
        else:
            unit = create_f(model, i)
        globals()[ident] = unit
        bar.next()
    bar.finish()

# This bit is special: Associate all rpms with the first repo,
# for max relational query fun
globals()['repository0'].add_units(*rpm.RPM.objects.all())
