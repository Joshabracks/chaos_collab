# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-07-25 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20190725_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collab',
            name='decoded_img',
            field=models.ImageField(upload_to='main_app/static/main_app/images'),
        ),
    ]