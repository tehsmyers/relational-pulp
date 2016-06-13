# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pulp.storage
import pulp.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checksum',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('object_id', models.UUIDField()),
                ('digest', models.CharField(max_length=63)),
                ('digest_type', pulp.fields.ChecksumTypeCharField(max_length=63)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
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
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_type', models.CharField(max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentUnitFile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.FileField(max_length=255, upload_to=pulp.storage.content_unit_path)),
                ('file_size', models.BigIntegerField()),
                ('unit', models.ForeignKey(related_name='files', to='pulp.ContentUnit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Importer',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
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
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
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
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('repo_id', models.CharField(unique=True, db_index=True, max_length=255)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
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
            field=models.ManyToManyField(related_name='repositories', through='pulp.RepositoryContentUnit', to='pulp.ContentUnit'),
        ),
        migrations.AddField(
            model_name='importer',
            name='repository',
            field=models.ForeignKey(to='pulp.Repository'),
        ),
    ]
