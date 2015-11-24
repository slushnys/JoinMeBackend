# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(to='ems.Location', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='postcode',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='street',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
