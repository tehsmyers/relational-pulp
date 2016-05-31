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

if platform.Repository.objects.count() < num_repos:
    num_repos -= platform.Repository.objects.count()
else:
    num_repos = 0

if rpm.RPM.objects.count() < num_rpm:
    num_rpm -= rpm.RPM.objects.count()
else:
    num_rpm = 0

if rpm.SRPM.objects.count() < num_srpm:
    num_srpm -= rpm.SRPM.objects.count()
else:
    num_srpm = 0

for i in range(num_repos):
    repo_name = coolname.generate_slug(2)
    repo_ident = 'repo{}'.format(i)
    repo, created = platform.Repository.objects.get_or_create(repo_id=repo_name)
    print('Repo {} created.'.format(repo_name), file=sys.stderr)
    globals()[repo_ident] = repo

for i in range(num_rpm):
    rpm_ident = 'rpm{}'.format(i)
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
    srpm_name = coolname.generate_slug(2)
    unit, created = rpm.SRPM.objects.get_or_create(
        name=srpm_name, epoch='epoch', version='version', release='release', arch='source')
    num_repos_added = int(random.random() * num_repos) + 1
    repos = platform.Repository.objects.all().order_by('?')[:num_repos_added]
    unit.repositories.add(*repos)
    print('SRPM {} created in {} repositories'.format(srpm_name, len(repos)),
          file=sys.stderr)
    globals()[srpm_ident] = unit

# clean up the namespace
try:
    del(repo)
    del(unit)
    del(num_repos_added)
except NameError:
    pass
