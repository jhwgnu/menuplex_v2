# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_restaurant_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='meal_date',
            field=models.DateField(),
        ),
    ]
