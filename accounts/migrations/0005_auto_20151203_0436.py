# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_country_currency'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalUserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=500)),
                ('profile_image', models.TextField(null=True, blank=True)),
                ('provider', models.TextField(null=True, verbose_name=b'provider', blank=True)),
                ('fullname', models.TextField(null=True, blank=True)),
                ('counts', models.TextField(null=True, blank=True)),
                ('posts', models.IntegerField(null=True, blank=True)),
                ('followers', models.IntegerField(null=True, blank=True)),
                ('numfollow', models.IntegerField(null=True, blank=True)),
                ('instagramid', models.TextField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='influencerprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='InfluencerProfile',
        ),
        migrations.RemoveField(
            model_name='weekcalendar',
            name='user',
        ),
        migrations.RemoveField(
            model_name='group',
            name='weeklycals',
        ),
        migrations.DeleteModel(
            name='WeekCalendar',
        ),
    ]
