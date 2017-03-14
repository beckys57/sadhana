# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-23 10:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='tree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trees.Tree'),
        ),
    ]
