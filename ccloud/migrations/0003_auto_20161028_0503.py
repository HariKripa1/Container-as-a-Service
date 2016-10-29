# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccloud', '0002_auto_20161026_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='openstack_user',
            name='password',
            field=models.CharField(default='password', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='openstack_user',
            name='username',
            field=models.CharField(default='user', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cluster',
            name='cluster_name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='status',
            field=models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_NODE_COMPLETE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_NODE_FAILED', 'Deletion in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Clutser creation failed'), ('STATUS_MODIFY_FAILED', 'Cluster redeployment failed'), ('STATUS_DELETE_FAILED', 'Cluster deletion failed')]),
        ),
        migrations.AlterField(
            model_name='node',
            name='master',
            field=models.CharField(max_length=1, choices=[('Y', 'Master'), ('N', 'Worker')]),
        ),
        migrations.AlterField(
            model_name='node',
            name='status',
            field=models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Node creation failed'), ('STATUS_MODIFY_FAILED', 'Node redeployment failed'), ('STATUS_DELETE_FAILED', 'Node deletion failed'), ('STATUS_DM_CREATED', 'Docker machine created'), ('STATUS_DM_FAILED', 'Docker machine failed')]),
        ),
    ]
