from rel_pulp import models

repo1, created = models.Repository.objects.get_or_create(repo_id='repo1')
repo2, created = models.Repository.objects.get_or_create(repo_id='repo2')

# rpm 1 is in repo 1 and 2
rpm1, created = models.RPM.objects.get_or_create(name='rpm1', epoch='e', version='v', release='r', arch='a')
rpm1.repositories.add(repo1, repo2)

# rpm 2 is in repo 1 only
rpm2, created = models.RPM.objects.get_or_create(name='rpm2', epoch='e', version='v', release='r', arch='a')
rpm2.repositories.add(repo1)

# rpm 3 is in repo 2 only
rpm3, created = models.RPM.objects.get_or_create(name='rpm3', epoch='e', version='v', release='r', arch='a')
rpm3.repositories.add(repo2)

# srpms are similarly joined to repos
srpm1, created = models.SRPM.objects.get_or_create(name='srpm1', epoch='e', version='v', release='r', arch='a')
srpm1.repositories.add(repo1, repo2)

srpm2, created = models.SRPM.objects.get_or_create(name='srpm2', epoch='e', version='v', release='r', arch='a')
srpm2.repositories.add(repo1)

srpm3, created = models.SRPM.objects.get_or_create(name='srpm3', epoch='e', version='v', release='r', arch='a')
srpm3.repositories.add(repo2)
