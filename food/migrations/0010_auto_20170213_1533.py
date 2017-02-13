# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_remove_meal_serving'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='soldout',
            field=models.BooleanField(default=True),
        ),
    ]
