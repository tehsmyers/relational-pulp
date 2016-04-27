from rel_pulp import models as platform
from rel_pulp_rpm import models as rpm

repo1, created = platform.Repository.objects.get_or_create(repo_id='repo1')
repo2, created = platform.Repository.objects.get_or_create(repo_id='repo2')

# rpm 1 is in repo 1 and 2
rpm1, created = rpm.RPM.objects.get_or_create(name='rpm1', epoch='e', version='v', release='r', arch='a')
rpm1.repositories.add(repo1, repo2)

# rpm 2 is in repo 1 only
rpm2, created = rpm.RPM.objects.get_or_create(name='rpm2', epoch='e', version='v', release='r', arch='a')
rpm2.repositories.add(repo1)

# rpm 3 is in repo 2 only
rpm3, created = rpm.RPM.objects.get_or_create(name='rpm3', epoch='e', version='v', release='r', arch='a')
rpm3.repositories.add(repo2)

# srpms are similarly joined to repos
srpm1, created = rpm.SRPM.objects.get_or_create(name='srpm1', epoch='e', version='v', release='r', arch='a')
srpm1.repositories.add(repo1, repo2)

srpm2, created = rpm.SRPM.objects.get_or_create(name='srpm2', epoch='e', version='v', release='r', arch='a')
srpm2.repositories.add(repo1)

srpm3, created = rpm.SRPM.objects.get_or_create(name='srpm3', epoch='e', version='v', release='r', arch='a')
srpm3.repositories.add(repo2)
