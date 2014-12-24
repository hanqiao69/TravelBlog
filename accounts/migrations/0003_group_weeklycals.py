# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_gen_first'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='weeklycals',
            field=models.ManyToManyField(related_name='groupcals', null=True, to='accounts.WeekCalendar', blank=True),
            preserve_default=True,
        ),
    ]
