# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pulp.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pulp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompsCategory',
            fields=[
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('category_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('display_order', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsEnvironment',
            fields=[
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('environment_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('display_order', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsGroup',
            fields=[
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('group_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('basearchonly', models.NullBooleanField(default=None)),
                ('default', models.BooleanField(default=False)),
                ('display_order', models.IntegerField()),
                ('user_visible', models.BooleanField(default=False)),
                ('langonly', models.CharField(max_length=63)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsGroupID',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsLangpacksMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('object_id', models.UUIDField()),
                ('name', models.CharField(max_length=255)),
                ('install', models.CharField(max_length=255)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompsOptionGroupID',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
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
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', parent_link=True, primary_key=True, auto_created=True, serialize=False)),
                ('distribution_id', models.CharField(max_length=255)),
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
            bases=('pulp.contentunit',),
        ),
        migrations.CreateModel(
            name='DRPM',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', parent_link=True, primary_key=True, auto_created=True, serialize=False)),
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
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('errata_id', models.CharField(max_length=255)),
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
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('short', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('errata', models.ForeignKey(to='pulp_rpm.Errata', related_name='pkglist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrataPackage',
            fields=[
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('name', models.CharField(max_length=255)),
                ('epoch', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=255)),
                ('release', models.CharField(max_length=255)),
                ('arch', models.CharField(max_length=255)),
                ('src', models.CharField(max_length=255)),
                ('filename', models.CharField(max_length=255)),
                ('digest', models.CharField(max_length=255)),
                ('collection', models.ForeignKey(to='pulp_rpm.ErrataCollection', related_name='packages')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrataReference',
            fields=[
                ('uuid', models.UUIDField(editable=False, serialize=False, primary_key=True, default=uuid.uuid4)),
                ('href', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=63)),
                ('id', models.CharField(max_length=63)),
                ('errata', models.ForeignKey(to='pulp_rpm.Errata', related_name='references')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ISO',
            fields=[
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', parent_link=True, primary_key=True, auto_created=True, serialize=False)),
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
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', parent_link=True, primary_key=True, auto_created=True, serialize=False)),
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
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', parent_link=True, primary_key=True, auto_created=True, serialize=False)),
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
                ('contentunit_ptr', models.OneToOneField(to='pulp.ContentUnit', parent_link=True, primary_key=True, auto_created=True, serialize=False)),
                ('data_type', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('pulp.contentunit',),
        ),
        migrations.CreateModel(
            name='YumRepository',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('pulp.repository',),
        ),
        migrations.AddField(
            model_name='compslangpacks',
            name='repository',
            field=models.ForeignKey(to='pulp_rpm.YumRepository'),
        ),
        migrations.AddField(
            model_name='compsgroup',
            name='repository',
            field=models.ForeignKey(to='pulp_rpm.YumRepository'),
        ),
        migrations.AddField(
            model_name='compsenvironment',
            name='repository',
            field=models.ForeignKey(to='pulp_rpm.YumRepository'),
        ),
        migrations.AddField(
            model_name='compscategory',
            name='repository',
            field=models.ForeignKey(to='pulp_rpm.YumRepository'),
        ),
    ]
