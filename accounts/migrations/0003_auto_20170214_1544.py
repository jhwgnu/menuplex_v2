# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-14 06:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170211_0247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='school',
            new_name='nickname',
        ),
    ]
