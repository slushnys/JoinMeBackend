# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 19:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20160715_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringauthenticationtoken',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 11, 19, 37, 10, 296067), verbose_name='Expires'),
        ),
    ]
