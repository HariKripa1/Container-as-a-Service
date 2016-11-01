# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccloud', '0004_auto_20161030_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='created_by_admin',
            field=models.CharField(default='N', max_length=1, choices=[('Y', 'Admin'), ('N', 'User')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cluster',
            name='master_name',
            field=models.CharField(default='A', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='container',
            name='container_or_service',
            field=models.CharField(default='C', max_length=100, choices=[('C', 'Container'), ('S', 'Service')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='container',
            name='port',
            field=models.CharField(default='5000', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='container',
            name='scale',
            field=models.CharField(default='2', max_length=100),
            preserve_default=False,
        ),
    ]
