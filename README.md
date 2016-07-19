Getting Started
===============

Install vagrant, and then `vagrant up`

SSH into the vagrant VM with `vagrant ssh`, switch to the relational-pulp virtualenv and start
a django shell with `workon rel-pulp` and `python manage.py shell`.


DB Management
=============

Reset the DB
------------

In vagrant, run the `db-reset.sh` script to populate the DB.

Populate the DB
---------------

`python manage.py runscript populate`

You can edit `scripts/populate.py` to customize DB population.


Fun Queries & Notable Objects
=============================

In the python shell, `from populate import *`

The populate script should be idempotent, and will ensure that the objects created within it exist
prior to using them in an interpreter. The script creates a few basic Repository and ContentUnit
instances, so print `globals()` to see what's available.

Repository Queries
------------------

To see all ContentUnits related to a repository:
```python
>>> repo0.units.all()
[<ContentUnit "rpm: rpm0-e-v-r-a">, ... ]
```
That isn't very special, here's the really cool thing we can do now, which is filter the units in
a repository by their fields
```python
>>> repo0.units.filter(rpm__name='rpm1')
[<ContentUnit "rpm: rpm0-e-v-r-a">, <ContentUnit "srpm: srpm1-e-v-r-a">]
```
Note the Django relational filter syntax, where rpm__name translates to "Filter by the name field
of rpm-type units." Just filtering by "name" does not work, because the relationship here is from
Repository to ContentUnit. So, this doesn't work:
```python
repo0.units.filter(name='rpm1')
(explosion!)
```
We could probably make it work with a fancy new custom filter method (this isn't entirely
unreasonable), but you can build a fancy query using Django "Q" objects, just like you do
in Mongoengine, which is Django's recommended solution to this problem:
```python
>>> from django.db.models import Q
>>> query = Q(rpm__name='rpm0')|Q(srpm_name='srpm1')
>>> repo0.units.filter(query)
>>> repo0.units.filter(query)
[<ContentUnit "rpm: rpm0-e-v-r-a">, <ContentUnit "srpm: srpm1-e-v-r-a">]
```
Note that those objects are current their generic ContentUnit instance type. Some customization has
been done to the content model to support casting those units as their final type. Doing this
returns an iterator of units (a list in this demo, can be a generator in the real thing), *not* a
queryset. No further filtering on the existing queryset can be done after casting the results to
their final unit type:
```python
>>> repo0.units.filter(query).cast()
[<RPM "rpm0-e-v-r-a">, <SRPM "srpm1-e-v-r-a">]
```
Instances of the final unit types inherit all properties of ContentUnits, so there should really
be no reason to "uncast" units. It is possible, however silly it might seem:
```python
>>> [unit.generic_unit() for unit in repo0.units.filter(query).cast()]
[<ContentUnit "rpm: rpm0-e-v-r-a">, <ContentUnit "srpm: srpm1-e-v-r-a">]
```
Note that repositories are never directly related to a typed content unit. If you
try to associate an RPM instance with a repository, Django will do its magical Django thing, see
that your RPM instance "is-a" ContentUnit, and make the relation correctly between Repository
and ContentUnit.

Another fun example query for repositories is getting the list of content types contained in that
repository:
```python
>>> repo0.units.distinct().values_list('content_type')
[(u'rpm',), (u'srpm',)]
```
And similarly, you can easily find repositories that only contain rpms:
```python
>>> models.Repository.objects.filter(units__content_type='rpm').distinct()
[<Repository "repo0">, <Repository "repo2">]
```
Unit Queries
------------

The Repositoy model's "units" related manager uses ContentUnit's queryset, so all queries done
on a repository's "units" attribute were technically unit queries. From the unit perspective,
depending on your usage you can either query the ContentUnit/Repository releationship generically,
or using a specific final unit type.

This will return all units in a repo:
```python
>>> models.ContentUnit.objects.filter(repositories__slug='repo0')
[<ContentUnit "rpm: rpm0-e-v-r-a">, ... ]
```
It is identical to running these commands:
```python
>>> models.Repository.objects.get(slug='repo0').units.all()
>>> repo0.units.all()
```
This will only return rpm-typed units in a repo; since their type is known, there is no need to
cast() them:
```python
>>> models.RPM.objects.filter(repositories__slug='repo0')
[<RPM "rpm0-e-v-r-a">, ... ]
```
When to query units directly or through a repository relationship is an implementation-specific
detail that needs to be decided on a case-by-case basis. Generally, when querying about units in a
specific repo (or repos), it will be easier to query through the repository model. When making
queries about all units known to pulp, it probably makes more sense to query through either the
generic content type model or through the final content type model.
