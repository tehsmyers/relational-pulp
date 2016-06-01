import random
import sys

import coolname

from pulp import models as platform
from pulp_rpm import models as rpm

# minimum number of things to cram into the db
num_repos = 10
num_rpm = 100
num_srpm = 10

# not DRY at all...
count_repos = platform.Repository.objects.count()
count_rpm = rpm.RPM.objects.count()
count_srpm = rpm.SRPM.objects.count()

for i in range(num_repos):
    repo_ident = 'repo{}'.format(i)
    if i < count_repos:
        repo = platform.Repository.objects.all()[i]
    else:
        repo_name = coolname.generate_slug(2)
        repo, created = platform.Repository.objects.get_or_create(repo_id=repo_name)
        print('Repo {} created.'.format(repo_name), file=sys.stderr)
    globals()[repo_ident] = repo

for i in range(num_rpm):
    rpm_ident = 'rpm{}'.format(i)
    if i < count_rpm:
        unit = rpm.RPM.objects.all()[i]
    else:
        rpm_name = coolname.generate_slug(2)
        unit, created = rpm.RPM.objects.get_or_create(
            name=rpm_name, epoch='epoch', version='version', release='release', arch='arch')
        num_repos_added = int(random.random() * num_repos) + 1
        repos = platform.Repository.objects.all().order_by('?')[:num_repos_added]
        unit.repositories.add(*repos)
        print('RPM {} created in {} repositories'.format(rpm_name, len(repos)),
              file=sys.stderr)
    globals()[rpm_ident] = unit

for i in range(num_srpm):
    srpm_ident = 'srpm{}'.format(i)
    if i < count_srpm:
        unit = rpm.SRPM.objects.all()[i]
    else:
        srpm_name = coolname.generate_slug(2)
        unit, created = rpm.SRPM.objects.get_or_create(
            name=srpm_name, epoch='epoch', version='version', release='release', arch='source')
        num_repos_added = int(random.random() * num_repos) + 1
        repos = platform.Repository.objects.all().order_by('?')[:num_repos_added]
        unit.repositories.add(*repos)
        print('SRPM {} created in {} repositories'.format(srpm_name, len(repos)),
              file=sys.stderr)
    globals()[srpm_ident] = unit
