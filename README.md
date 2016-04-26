Getting Started
===============

To get started, have django create the db:
```
python manage.py migrate --run-syncdb
```
Now, populate it.

In an interpreter, you can "from populate import *", or you can set PYTHONSTARTUP and have python
run the populate script for you before starting the interpreter, e.g.
```
PYTHONSTARTUP=populate.py python manage.py shell
```
If you have ipython installed, the django shell will use it. (You should have ipython installed)

To reset, `rm db.sqlite3` and restart your interpreter.

Fun Queries & Notable Objects
=============================

The populate script should be idempotent, and will ensure that the objects created within it exist
prior to using them in an interpreter. The script creates a few basic Repository and ContenUnit
instances, so take a peek in there to see what it's doing to find out everything that's available.

Repository Queries
------------------

To see all ContentUnits related to a repository:
```python
>>> repo1.units.all()
[<ContentUnit "rpm: rpm1-e-v-r-a">, ... ]
```
That isn't very special, here's the really cool thing we can do now, which is filter the units in
a repository by their fields
```python
>>> repo1.units.filter(rpm__name='rpm2')
[<ContentUnit "rpm: rpm1-e-v-r-a">, <ContentUnit "srpm: srpm2-e-v-r-a">]
```
Note the Django relational filter syntax, where rpm__name translates to "Filter by the name field
of rpm-type units." Just filtering by "name" does not work, because the relationship here is from
Repository to ContentUnit. So, this doesn't work:
```python
repo1.units.filter(name='rpm2')
(explosion!)
```
We could probably make it work with a fancy new custom filter method (this isn't entirely
unreasonable), but you can build a fancy query using Django "Q" objects, just like you do
in Mongoengine, which is Django's recommended solution to this problem:
```python
>>> from django.db.models import Q
>>> query = Q(rpm__name='rpm1')|Q(srpm_name='srpm2')
>>> repo1.units.filter(query)
>>> repo1.units.filter(query)
[<ContentUnit "rpm: rpm1-e-v-r-a">, <ContentUnit "srpm: srpm2-e-v-r-a">]
```
Note that those objects are current their generic ContentUnit instance type. Some customization has
been done to the content model to support casting those units as their final type. Doing this
returns an iterator of units (a list in this demo, can be a generator in the real thing), *not* a
queryset. No further filtering on the existing queryset can be done after casting the results to
their final unit type:
```python
>>> repo1.units.filter(query).cast()
[<RPM "rpm1-e-v-r-a">, <SRPM "srpm2-e-v-r-a">]
```
Instances of the final unit types inherit all properties of ContentUnits, so there should really
be no reason to "uncast" units. It is possible, however silly it might seem:
```python
>>> [unit.generic_unit() for unit in repo1.units.filter(query).cast()]
[<ContentUnit "rpm: rpm1-e-v-r-a">, <ContentUnit "srpm: srpm2-e-v-r-a">]
```
Note that repositories are never directly related to a typed content unit. If you
try to associate an RPM instance with a repository, Django will do its magical Django thing, see
that your RPM instance "is-a" ContentUnit, and make the relation correctly between Repository
and ContentUnit.

Another fun example query for repositories is getting the list of content types contained in that
repository:
```python
>>> repo1.units.distinct().values_list('content_type')
[(u'rpm',), (u'srpm',)]
```
And similarly, you can easily find repositories that only contain rpms:
```python
>>> models.Repository.objects.filter(units__content_type='rpm').distinct()
[<Repository "repo1">, <Repository "repo2">]
```
Unit Queries
------------

The Repositoy model's "units" related manager uses ContentUnit's queryset, so all queries done
on a repository's "units" attribute were technically unit queries. From the unit perspective,
depending on your usage you can either query the ContentUnit/Repository releationship generically,
or using a specific final unit type.

This will return all units in a repo:
```python
>>> models.ContentUnit.objects.filter(repositories__repo_id='repo1')
[<ContentUnit "rpm: rpm1-e-v-r-a">, ... ]
```
It is identical to running these commands:
```python
>>> models.Repository.objects.get(repo_id='repo1').units.all()
>>> repo1.units.all()
```
This will only return rpm-typed units in a repo; since their type is known, there is no need to
cast() them:
```python
>>> models.RPM.objects.filter(repositories__repo_id='repo1')
[<RPM "rpm1-e-v-r-a">, ... ]
```
When to query units directly or through a repository relationship is an implementation-specific
detail that needs to be decided on a case-by-case basis. Generally, when querying about units in a
specific repo (or repos), it will be easier to query through the repository model. When making
queries about all units known to pulp, it probably makes more sense to query through either the
generic content type model or through the final content type model.
