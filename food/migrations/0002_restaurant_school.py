# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='school',
            field=models.ForeignKey(default=1, to='food.School'),
            preserve_default=False,
        ),
    ]
