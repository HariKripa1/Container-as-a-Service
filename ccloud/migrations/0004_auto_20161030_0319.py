# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccloud', '0003_auto_20161028_0503'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='cluster_id',
            field=models.ForeignKey(default=1, to='ccloud.Cluster'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cluster',
            name='status',
            field=models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_NODE_COMPLETE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_NODE_FAILED', 'Deletion in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Clutser creation failed'), ('STATUS_MODIFY_FAILED', 'Cluster redeployment failed'), ('STATUS_DELETE_FAILED', 'Cluster deletion failed'), ('STATUS_DM_CREATED', 'Docker machine created'), ('STATUS_DM_FAILED', 'Docker machine failed'), ('STATUS_SWARM_CREATED', 'Docker swarm created'), ('STATUS_SWARM_FAILED', 'Docker swarm failed')]),
        ),
        migrations.AlterField(
            model_name='node',
            name='status',
            field=models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Node creation failed'), ('STATUS_MODIFY_FAILED', 'Node redeployment failed'), ('STATUS_DELETE_FAILED', 'Node deletion failed'), ('STATUS_DM_CREATED', 'Docker machine created'), ('STATUS_DM_FAILED', 'Docker machine failed'), ('STATUS_SWARM_CREATED', 'Docker swarm created'), ('STATUS_SWARM_FAILED', 'Docker swarm failed')]),
        ),
    ]
