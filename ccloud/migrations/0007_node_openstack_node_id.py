# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccloud', '0006_auto_20161101_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='openstack_node_id',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
