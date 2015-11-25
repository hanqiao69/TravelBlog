# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_influencerprofile_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=3)),
                ('name', models.CharField(max_length=500)),
                ('temperature', models.TextField(null=True, blank=True)),
                ('rainfall', models.TextField(null=True, blank=True)),
                ('rainy_dry', models.TextField(null=True, blank=True)),
                ('safety', models.FloatField(null=True, blank=True)),
                ('health', models.FloatField(null=True, blank=True)),
                ('internet', models.FloatField(null=True, blank=True)),
                ('travel', models.FloatField(null=True, blank=True)),
                ('openness', models.FloatField(null=True, blank=True)),
                ('price', models.FloatField(null=True, blank=True)),
                ('environment', models.FloatField(null=True, blank=True)),
                ('air', models.FloatField(null=True, blank=True)),
                ('ground', models.FloatField(null=True, blank=True)),
                ('tourist', models.FloatField(null=True, blank=True)),
                ('nature', models.FloatField(null=True, blank=True)),
                ('culture', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=3)),
                ('name', models.CharField(max_length=500)),
                ('current', models.FloatField(null=True, blank=True)),
                ('current_updated', models.DateField(null=True, blank=True)),
                ('five_yr_mean', models.FloatField(null=True, blank=True)),
                ('five_yr_stdev', models.FloatField(null=True, blank=True)),
                ('z_score', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
