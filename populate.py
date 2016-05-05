import random
import sys

from rel_pulp import models as platform
from rel_pulp_rpm import models as rpm

num_repos = 10
num_rpm = 20
num_srpm = 10

for i in range(num_repos):
    repo_id = 'repo{}'.format(i)
    repo, created = platform.Repository.objects.get_or_create(repo_id=repo_id)
    if created:
        print('Repo {} created.'.format(repo_id), file=sys.stderr)
    globals()[repo_id] = repo

for i in range(num_rpm):
    rpm_name = 'rpm{}'.format(i)
    unit, created = rpm.RPM.objects.get_or_create(
        name=rpm_name, epoch='epoch', version='version', release='release', arch='arch')
    num_repos_added = int(random.random() * num_repos)
    if created:
        repos = platform.Repository.objects.all().order_by('?')[:num_repos_added]
        unit.repositories.add(*repos)
        print('RPM {} created in {} repositories'.format(rpm_name, len(repos)),
              file=sys.stderr)
    globals()[rpm_name] = unit

for i in range(num_srpm):
    srpm_name = 'srpm{}'.format(i)
    unit, created = rpm.SRPM.objects.get_or_create(
        name=srpm_name, epoch='epoch', version='version', release='release', arch='source')
    num_repos_added = int(random.random() * num_repos)
    if created:
        repos = platform.Repository.objects.all().order_by('?')[:num_repos_added]
        unit.repositories.add(*repos)
        print('SRPM {} created in {} repositories'.format(srpm_name, len(repos)),
              file=sys.stderr)
    globals()[srpm_name] = unit

# clean up the namespace
del(repo)
del(unit)
del(num_repos_added)
