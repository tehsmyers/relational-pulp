# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pulp.storage
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
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
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('content_type', models.CharField(max_length=15)),
                ('key_digest', models.CharField(max_length=64, db_index=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentUnitFile',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('content', models.FileField(max_length=255, upload_to=pulp.storage.content_unit_path)),
                ('downloaded', models.BooleanField(default=False)),
                ('file_size', models.BigIntegerField()),
                ('md5', models.CharField(max_length=32, blank=True, null=True)),
                ('sha1', models.CharField(max_length=40, blank=True, null=True)),
                ('sha256', models.CharField(max_length=64, blank=True, null=True)),
                ('sha512', models.CharField(max_length=128, blank=True, null=True)),
                ('unit', models.ForeignKey(related_name='files', to='pulp.ContentUnit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Importer',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('importer_type_id', models.CharField(max_length=255)),
                ('last_sync', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
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
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('repo_id', models.CharField(max_length=255, db_index=True, unique=True)),
                ('display_name', models.CharField(max_length=255, blank=True, default='')),
                ('description', models.TextField(blank=True, default='')),
                ('last_unit_added', models.DateTimeField(blank=True, null=True)),
                ('last_unit_removed', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RepositoryContentUnit',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('content_unit', models.ForeignKey(to='pulp.ContentUnit')),
                ('repository', models.ForeignKey(to='pulp.Repository')),
            ],
            options={
                'ordering': ['updated'],
                'get_latest_by': 'updated',
            },
        ),
        migrations.CreateModel(
            name='Scratchpad',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
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
            field=models.ManyToManyField(related_name='repositories', to='pulp.ContentUnit', through='pulp.RepositoryContentUnit'),
        ),
        migrations.AddField(
            model_name='importer',
            name='repository',
            field=models.ForeignKey(related_name='importers', to='pulp.Repository'),
        ),
        migrations.AlterUniqueTogether(
            name='repositorycontentunit',
            unique_together=set([('repository', 'content_unit')]),
        ),
    ]
