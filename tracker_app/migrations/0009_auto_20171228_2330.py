# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-28 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0008_auto_20171228_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='timestamp_last_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]