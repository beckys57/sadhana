# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-10 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0003_auto_20170223_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='tree',
            name='number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
