# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencerprofile',
            name='provider',
            field=models.TextField(null=True, verbose_name=b'provider', blank=True),
            preserve_default=True,
        ),
    ]
