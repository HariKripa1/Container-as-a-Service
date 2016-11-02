# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccloud', '0005_auto_20161031_0739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='cluster_name',
            field=models.CharField(max_length=200),
        ),
    ]
