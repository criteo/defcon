# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0012_auto_20170418_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plugin',
            name='contact',
        ),
        migrations.AlterField(
            model_name='plugin',
            name='link',
            field=models.URLField(blank=True, max_length=254),
        ),
    ]
