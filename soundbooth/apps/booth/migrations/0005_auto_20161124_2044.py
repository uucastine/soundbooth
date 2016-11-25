# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-25 01:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0004_schedule_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='Time to record'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateTimeField(blank=True, help_text='One-off recording date, can be blank for recurring events.', null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='rule',
            field=models.CharField(blank=True, help_text='A human-readable pattern for recurring schedules', max_length=255, null=True, verbose_name='Recurring rule'),
        ),
    ]
