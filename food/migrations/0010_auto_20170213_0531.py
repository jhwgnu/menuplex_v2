# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-13 05:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0009_comment_school'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ['-id']},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='school',
        ),
    ]