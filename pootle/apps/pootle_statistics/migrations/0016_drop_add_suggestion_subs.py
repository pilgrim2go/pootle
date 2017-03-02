# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 11:10
from __future__ import unicode_literals

from django.db import migrations


SUGG_ADD_FLAG = 8


def drop_add_suggestion_subs(apps, schema_editor):
    subs = apps.get_model("pootle_statistics.Submission").objects.all()
    subs.filter(type=SUGG_ADD_FLAG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_statistics', '0015_remove_system_scorelogs'),
    ]

    operations = [
        migrations.RunPython(drop_add_suggestion_subs),
    ]