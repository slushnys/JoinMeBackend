# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hashtags', '0001_initial'),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('uuid', models.UUIDField(serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('description', models.TextField()),
                ('status', models.IntegerField()),
                ('datetime', models.DateTimeField()),
                ('begin_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Hashtags',
            fields=[
                ('uuid', models.UUIDField(serialize=False, editable=False, primary_key=True)),
                ('event', models.ForeignKey(to='ems.Event')),
                ('hashtag', models.ForeignKey(to='hashtags.Hashtag')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('uuid', models.UUIDField(serialize=False, editable=False, primary_key=True)),
                ('account', models.ForeignKey(to='crm.Account')),
                ('event', models.ForeignKey(to='ems.Event')),
            ],
        ),
    ]
