# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20170207_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meal',
            name='price',
        ),
    ]
