# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 03:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muzik', '0003_auto_20170928_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='release_date',
        ),
    ]