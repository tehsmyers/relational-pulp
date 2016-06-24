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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('uuid', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
                ('content_type', models.CharField(max_length=15)),
                ('key_digest', models.CharField(db_index=True, unique=True, max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentUnitFile',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
                ('content', models.FileField(upload_to=pulp.storage.content_unit_path, max_length=255)),
                ('downloaded', models.BooleanField(default=False)),
                ('file_size', models.BigIntegerField()),
                ('md5', models.CharField(blank=True, null=True, max_length=32)),
                ('sha1', models.CharField(blank=True, null=True, max_length=40)),
                ('sha224', models.CharField(blank=True, null=True, max_length=56)),
                ('sha256', models.CharField(blank=True, null=True, max_length=64)),
                ('sha384', models.CharField(blank=True, null=True, max_length=96)),
                ('sha512', models.CharField(blank=True, null=True, max_length=128)),
                ('unit', models.ForeignKey(related_name='files', to='pulp.ContentUnit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataTypesDemo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('smallint', models.SmallIntegerField()),
                ('integer', models.IntegerField()),
                ('bigint', models.BigIntegerField()),
                ('psmallint', models.PositiveSmallIntegerField()),
                ('pint', models.PositiveIntegerField()),
                ('floatfield', models.FloatField()),
                ('decimal', models.DecimalField(max_digits=5, decimal_places=3)),
                ('binary', models.BinaryField()),
                ('dt', models.DateTimeField()),
                ('d', models.DateField()),
                ('t', models.TimeField()),
                ('boolean', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Importer',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
                ('uuid', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
                ('repo_id', models.CharField(db_index=True, unique=True, max_length=255)),
                ('display_name', models.CharField(blank=True, default='', max_length=255)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
