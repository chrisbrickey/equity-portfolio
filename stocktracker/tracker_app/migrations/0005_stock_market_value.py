# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-28 19:38
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker_app', '0004_auto_20171228_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='market_value',
            field=models.DecimalField(decimal_places=3, default=Decimal('0.000'), max_digits=19),
        ),
    ]