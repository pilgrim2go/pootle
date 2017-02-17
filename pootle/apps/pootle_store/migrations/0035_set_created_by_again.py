# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 21:46
from __future__ import unicode_literals

import logging
import time

from django.db import migrations

from pootle.core.user import get_system_user_id
from pootle_statistics.models import SubmissionTypes


logger = logging.getLogger(__name__)


def set_unit_created_by(apps, schema_editor):
    subs = apps.get_model("pootle_statistics.Submission").objects.all()
    UnitSource = apps.get_model("pootle_store.UnitSource")
    sources = UnitSource.objects.all()
    units = apps.get_model("pootle_store.Unit").objects.all()
    total = units.count()
    offset = 0
    step = 10000
    start = time.time()
    creators = dict(
        subs.filter(type=SubmissionTypes.UNIT_CREATE)
            .exclude(submitter__username="system")
            .values_list("unit_id", "submitter"))
    sysuser = get_system_user_id()

    while True:
        UnitSource.objects.bulk_create(
            [UnitSource(
                unit_id=pk,
                created_by_id=creators.get(pk, sysuser))
             for pk
             in units[offset: offset + step].values_list("id", flat=True)])
        logger.debug(
            "added %s/%s in %s seconds"
            % (offset + step, total, (time.time() - start)))
        if offset > total:
            break
        offset = offset + step


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_store', '0034_unitsource'),
    ]

    operations = [
        migrations.RunPython(set_unit_created_by),
]