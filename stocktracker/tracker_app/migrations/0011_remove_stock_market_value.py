# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-30 02:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0010_remove_stock_company_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='market_value',
        ),
    ]
