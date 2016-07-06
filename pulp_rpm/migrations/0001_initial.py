# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pulp.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pulp', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comps',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsCategory',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('display_order', models.IntegerField()),
                ('parent', models.ForeignKey(related_name='categories', to='pulp_rpm.Comps')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsEnvironment',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('display_order', models.IntegerField()),
                ('parent', models.ForeignKey(related_name='environments', to='pulp_rpm.Comps')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsGroup',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('basearchonly', models.NullBooleanField(default=None)),
                ('default', models.BooleanField(default=False)),
                ('display_order', models.IntegerField()),
                ('user_visible', models.BooleanField(default=False)),
                ('langonly', models.CharField(max_length=63)),
                ('parent', models.ForeignKey(related_name='groups', to='pulp_rpm.Comps')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsGroupID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.UUIDField()),
                ('name', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsLangpacks',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('parent', models.ForeignKey(related_name='langpacks', to='pulp_rpm.Comps')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsLangpacksMatch',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('install', models.CharField(max_length=255)),
                ('langpack', models.ForeignKey(related_name='matches', to='pulp_rpm.CompsLangpacks')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsOptionGroupID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.UUIDField()),
                ('name', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsPackageReq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.UUIDField()),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=63)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsTranslatedDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.UUIDField()),
                ('lang', models.CharField(max_length=63)),
                ('value', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsTranslatedName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.UUIDField()),
                ('lang', models.CharField(max_length=63)),
                ('value', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('slug', models.SlugField(unique=True)),
                ('family', models.CharField(max_length=255)),
                ('variant', models.CharField(max_length=255, blank=True)),
                ('version', models.CharField(max_length=255)),
                ('arch', models.CharField(max_length=255)),
                ('timestamp', models.FloatField()),
                ('packagedir', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp.contentunit', models.Model),
        ),
        migrations.CreateModel(
            name='DRPM',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('version', models.CharField(max_length=63)),
                ('release', models.CharField(max_length=63)),
                ('checksum', models.CharField(max_length=255)),
                ('checksumtype', pulp.fields.ChecksumTypeCharField(max_length=63)),
                ('version_sort_index', models.CharField(max_length=63)),
                ('release_sort_index', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp.contentunit',),
        ),
        migrations.CreateModel(
            name='Errata',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('issued', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('description', models.TextField()),
                ('solution', models.TextField()),
                ('summary', models.TextField()),
                ('pushcount', models.PositiveIntegerField()),
                ('reboot_suggested', models.BooleanField(default=False)),
                ('errata_from', models.CharField(max_length=255)),
                ('severity', models.CharField(max_length=255)),
                ('rights', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('release', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrataCollection',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('short', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('errata', models.ForeignKey(related_name='pkglist', to='pulp_rpm.Errata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrataPackage',
            fields=[
                ('uuid', models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('epoch', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('release', models.CharField(max_length=255)),
                ('arch', models.CharField(max_length=255)),
                ('src', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('sum', models.CharField(max_length=255)),
                ('sum_type', models.CharField(max_length=255)),
                ('collection', models.ForeignKey(related_name='packages', to='pulp_rpm.ErrataCollection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrataReference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.UUIDField()),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('href', models.TextField()),
                ('type', models.CharField(max_length=63)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('errata', models.ForeignKey(related_name='references', to='pulp_rpm.Errata')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrataReferenceAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.UUIDField()),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ISO',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp.contentunit',),
        ),
        migrations.CreateModel(
            name='RPM',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('version', models.CharField(max_length=63)),
                ('release', models.CharField(max_length=63)),
                ('checksum', models.CharField(max_length=255)),
                ('checksumtype', pulp.fields.ChecksumTypeCharField(max_length=63)),
                ('version_sort_index', models.CharField(max_length=63)),
                ('release_sort_index', models.CharField(max_length=63)),
                ('name', models.CharField(max_length=127)),
                ('epoch', models.CharField(max_length=63)),
                ('arch', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp.contentunit',),
        ),
        migrations.CreateModel(
            name='SRPM',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('version', models.CharField(max_length=63)),
                ('release', models.CharField(max_length=63)),
                ('checksum', models.CharField(max_length=255)),
                ('checksumtype', pulp.fields.ChecksumTypeCharField(max_length=63)),
                ('version_sort_index', models.CharField(max_length=63)),
                ('release_sort_index', models.CharField(max_length=63)),
                ('name', models.CharField(max_length=127)),
                ('epoch', models.CharField(max_length=63)),
                ('arch', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp.contentunit',),
        ),
        migrations.CreateModel(
            name='YumMetadataFile',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', auto_created=True, primary_key=True, serialize=False, parent_link=True)),
                ('data_type', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp.contentunit',),
        ),
        migrations.CreateModel(
            name='RPMRepositoryProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('pulp.repository',),
        ),
        migrations.AddField(
            model_name='errata',
            name='repository',
            field=models.ForeignKey(related_name='errata', to='pulp_rpm.RPMRepositoryProxy'),
        ),
        migrations.AddField(
            model_name='comps',
            name='repository',
            field=models.OneToOneField(related_name='comps', to='pulp_rpm.RPMRepositoryProxy'),
        ),
        migrations.AlterUniqueTogether(
            name='erratareferenceattributes',
            unique_together=set([('key', 'content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='erratareference',
            unique_together=set([('key', 'content_type', 'object_id')]),
        ),
    ]
