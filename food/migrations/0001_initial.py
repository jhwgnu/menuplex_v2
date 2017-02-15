# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import food.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=800)),
                ('time', models.CharField(max_length=10, choices=[('morning', '조식'), ('lunch', '중식'), ('dinner', '석식')], default='lunch')),
                ('meal_date', models.DateField()),
                ('soldout', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Mealcomment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('meal', models.ForeignKey(to='food.Meal')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('lnglat', models.CharField(max_length=50, blank=True, validators=[food.models.lnglat_validator])),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('school_url', models.URLField()),
                ('shortname', models.CharField(max_length=10)),
                ('logo', models.ImageField(upload_to='')),
                ('center', models.CharField(max_length=50, blank=True, validators=[food.models.lnglat_validator])),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='school',
            field=models.ForeignKey(to='food.School'),
        ),
        migrations.AddField(
            model_name='meal',
            name='restaurant',
            field=models.ForeignKey(to='food.Restaurant'),
        ),
        migrations.AddField(
            model_name='meal',
            name='school',
            field=models.ForeignKey(to='food.School'),
        ),
        migrations.AddField(
            model_name='comment',
            name='restaurant',
            field=models.ForeignKey(to='food.Restaurant'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
