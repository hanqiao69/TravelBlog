# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_normaluserprofile_search_cache'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currency',
            old_name='five_yr_stdev',
            new_name='percent_change',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='z_score',
        ),
    ]
