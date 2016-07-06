# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
import pulp.storage


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
            name='ContentUnit',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('content_type', models.CharField(max_length=15)),
                ('key_digest', models.CharField(unique=True, max_length=64, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentUnitFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('content', models.FileField(max_length=255, upload_to=pulp.storage.content_unit_path)),
                ('downloaded', models.BooleanField(default=False)),
                ('file_size', models.BigIntegerField()),
                ('md5', models.CharField(max_length=32, null=True, blank=True)),
                ('sha1', models.CharField(max_length=40, null=True, blank=True)),
                ('sha224', models.CharField(max_length=56, null=True, blank=True)),
                ('sha256', models.CharField(max_length=64, null=True, blank=True)),
                ('sha384', models.CharField(max_length=96, null=True, blank=True)),
                ('sha512', models.CharField(max_length=128, null=True, blank=True)),
                ('unit', models.ForeignKey(to='pulp.ContentUnit', related_name='files')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataTypesDemo',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('smallint', models.SmallIntegerField()),
                ('integer', models.IntegerField()),
                ('bigint', models.BigIntegerField()),
                ('psmallint', models.PositiveSmallIntegerField()),
                ('pint', models.PositiveIntegerField()),
                ('floatfield', models.FloatField()),
                ('decimal', models.DecimalField(decimal_places=3, max_digits=5)),
                ('binary', models.BinaryField()),
                ('dt', models.DateTimeField()),
                ('d', models.DateField()),
                ('t', models.TimeField()),
                ('boolean', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Importer',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('importer_type_id', models.CharField(max_length=255)),
                ('last_sync', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
            name='Repository',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('slug', models.SlugField(unique=True)),
                ('display_name', models.CharField(default='', max_length=255, blank=True)),
                ('description', models.TextField(default='', blank=True)),
                ('last_unit_added', models.DateTimeField(null=True, blank=True)),
                ('last_unit_removed', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RepositoryContentUnit',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, serialize=False, primary_key=True, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content_unit', models.ForeignKey(to='pulp.ContentUnit')),
                ('repository', models.ForeignKey(to='pulp.Repository')),
            ],
            options={
                'get_latest_by': 'updated',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Scratchpad',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('object_id', models.UUIDField()),
                ('key', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='repository',
            name='units',
            field=models.ManyToManyField(through='pulp.RepositoryContentUnit', to='pulp.ContentUnit', related_name='repositories'),
        ),
        migrations.AddField(
            model_name='importer',
            name='repository',
            field=models.ForeignKey(to='pulp.Repository', related_name='importers'),
        ),
        migrations.AlterUniqueTogether(
            name='scratchpad',
            unique_together=set([('key', 'content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='repositorycontentunit',
            unique_together=set([('repository', 'content_unit')]),
        ),
        migrations.AlterUniqueTogether(
            name='notes',
            unique_together=set([('key', 'content_type', 'object_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='config',
            unique_together=set([('key', 'content_type', 'object_id')]),
        ),
    ]
