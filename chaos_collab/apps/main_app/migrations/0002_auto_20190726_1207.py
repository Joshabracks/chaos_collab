# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-26 19:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pkey',
            name='child',
        ),
        migrations.RemoveField(
            model_name='pkey',
            name='parent',
        ),
        migrations.AddField(
            model_name='collab',
            name='parent',
            field=models.CharField(blank=True, max_length=45),
        ),
        migrations.DeleteModel(
            name='Pkey',
        ),
    ]