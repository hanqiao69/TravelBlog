# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20151203_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='normaluserprofile',
            name='search_cache',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
