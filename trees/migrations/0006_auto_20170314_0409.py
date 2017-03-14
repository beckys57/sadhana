# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trees', '0005_auto_20170310_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='reason_dead',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(1, 'moved'), (2, 'animals'), (3, 'children'), (4, 'termites'), (5, 'salt'), (6, 'dryness'), (7, 'no water'), (8, 'dry'), (9, 'conflict'), (10, 'syz')]),
        ),
    ]
