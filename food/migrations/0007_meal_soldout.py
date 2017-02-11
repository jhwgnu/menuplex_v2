# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_auto_20170210_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='soldout',
            field=models.BooleanField(default=False),
        ),
    ]
