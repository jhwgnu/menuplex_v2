# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import food.models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0022_school_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='lnglat',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='lnglat',
            field=models.CharField(blank=True, validators=[food.models.lnglat_validator], max_length=50),
        ),
        migrations.AddField(
            model_name='school',
            name='lnglat',
            field=models.CharField(blank=True, validators=[food.models.lnglat_validator], max_length=50),
        ),
    ]
