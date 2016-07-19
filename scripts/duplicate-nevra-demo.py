# call this with `python manage.py runscript duplicate-nevra-demo`

import random
import time

from pulp_rpm.models import RPM, RPMRepositoryProxy

# don't make more duplicates than this in a single repo
repo_max_duplicates = 100


# the actual duplicate nevra killer
def duplicate_nevra_detector(repo):
    print('Calculating duplicates for repo {}'.format(repo.slug), end='', flush=True)
    seen_nevra = set()
    duplicate_nevra = set()
    # sift rpms to find duplicate nevra in a repo
    for rpm in RPM.objects.filter(repositories=repo):
        nevra = rpm.nevra_tuple
        if nevra in seen_nevra:
            duplicate_nevra.add(nevra)
        else:
            seen_nevra.add(nevra)
    # get a list of packages matching this nevra sorted by their updated timestamp, descending (newest first)
    removed_dupes = 0
    for nevra in duplicate_nevra:
        packages = RPM.objects.filter(repositories=repo, **nevra._asdict()).order_by('-repositorycontentunit__updated')
        duplicates = packages[1:]
        repo.remove_units(*duplicates)
        removed_dupes += len(duplicates)
    print(': removed {} duplicate RPMs.'.format(removed_dupes))


def run():
    print('Creating duplicate NEVRA in all repos')
    # stash the duplicates we create in a set of dupe tuples for later assertion
    dupe_map = []

    # duplicate nevra maker, creates dupes in each repo to clean up
    for repo in RPMRepositoryProxy.objects.all():
        # create a random number of duplicates based on 10% of the number of packages in the repo
        num_dupes = 0
        max_dupes = int(repo_max_duplicates * random.random())
        # make some duplicate nevra...
        random_rpms = RPM.objects.filter(repositories=repo).order_by('?')

        for rpm in random_rpms:
            # we potentially create multiple new rpms, only the newest (last created) one should surive
            # so track the "old" pks for asserting later
            rpm_pks = [rpm.pk]
            # create 1-3 duplicates for each rpm chosen to duplicate
            for i in range(random.randint(1, 3)):
                # use timestamp + i to get a unique "checksum" value and bypass the unit key uniqueness constraint
                new_rpm = RPM.objects.create(checksum=str(time.time() + i), **rpm.nevra_tuple._asdict())
                new_rpm.add_repos(repo)
                rpm_pks.append(new_rpm.pk)
                num_dupes += 1

            # The old PKs are everything up to the last element of our list, the one to keep is the last one added
            dupe_map.append((repo, rpm_pks[:-1], rpm_pks[-1]))
            # this can actually be less then 0 since we don't check num_dupes in the new_rpm creation loop
            if num_dupes >= max_dupes:
                break

        print('{} Duplicate NEVRA RPMs in repo {}'.format(num_dupes, repo.slug))

    print('Created {} total duplicate NEVRA RPMs.'.format(len(dupe_map)))

    # run it!
    print('Destroying duplicate NEVRA in all repos')
    for repo in RPMRepositoryProxy.objects.all():
        duplicate_nevra_detector(repo)

    print('Asserting no duplicates remain')
    for repo, old_pks, new_pk in dupe_map:
        for old_pk in old_pks:
            assert not repo.units.filter(pk=old_pk).exists()
        assert repo.units.filter(pk=new_pk).exists()
    print('All duplicates removed')
