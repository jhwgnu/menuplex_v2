# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0013_auto_20170213_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='name',
            field=models.CharField(max_length=400),
        ),
    ]
