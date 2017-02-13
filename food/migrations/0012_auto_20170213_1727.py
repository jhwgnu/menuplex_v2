# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0011_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='soldout',
            field=models.BooleanField(default=False),
        ),
    ]
