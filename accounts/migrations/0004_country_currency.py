# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151125_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.ManyToManyField(to='accounts.Currency', null=True, blank=True),
            preserve_default=True,
        ),
    ]
