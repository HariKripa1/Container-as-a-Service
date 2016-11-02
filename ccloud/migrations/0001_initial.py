# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cluster_name', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_NODE_COMPLETE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_NODE_FAILED', 'Deletion in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Clutser creation failed'), ('STATUS_MODIFY_FAILED', 'Cluster redeployment failed'), ('STATUS_DELETE_FAILED', 'Cluster deletion failed'), ('STATUS_DM_CREATED', 'Docker machine created'), ('STATUS_DM_FAILED', 'Docker machine failed'), ('STATUS_SWARM_CREATED', 'Docker swarm created'), ('STATUS_SWARM_FAILED', 'Docker swarm failed')])),
                ('no_of_instances', models.IntegerField()),
                ('requested_no_of_instance', models.IntegerField()),
                ('master_ip', models.CharField(max_length=200)),
                ('master_name', models.CharField(max_length=200)),
                ('token_id', models.CharField(max_length=500)),
                ('creation_date', models.DateTimeField(verbose_name='date created')),
                ('last_update_date', models.DateTimeField(verbose_name='date updated')),
                ('created_by', models.CharField(max_length=100)),
                ('created_by_admin', models.CharField(max_length=1, choices=[('Y', 'Admin'), ('N', 'User')])),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('container_name', models.CharField(max_length=200)),
                ('git_url', models.CharField(max_length=1000)),
                ('docker_file', models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])),
                ('application_name', models.CharField(max_length=100, choices=[('APPLICATION_NODE_JS', 'Node JS')])),
                ('status', models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Container creation failed'), ('STATUS_MODIFY_FAILED', 'Container redeployment failed'), ('STATUS_DELETE_FAILED', 'Container deletion failed')])),
                ('container_url', models.CharField(max_length=1000)),
                ('devstack_container_id', models.CharField(max_length=1000)),
                ('creation_date', models.DateTimeField(verbose_name='date created')),
                ('last_update_date', models.DateTimeField(verbose_name='date updated')),
                ('created_by', models.CharField(max_length=100)),
                ('container_or_service', models.CharField(max_length=100, choices=[('C', 'Container'), ('S', 'Service')])),
                ('port', models.CharField(max_length=100)),
                ('scale', models.CharField(max_length=100)),
                ('cluster_id', models.ForeignKey(related_name='containers', to='ccloud.Cluster')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('machine_ip', models.CharField(max_length=200)),
                ('master', models.CharField(max_length=1, choices=[('Y', 'Master'), ('N', 'Worker')])),
                ('machine_name', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Node creation failed'), ('STATUS_MODIFY_FAILED', 'Node redeployment failed'), ('STATUS_DELETE_FAILED', 'Node deletion failed'), ('STATUS_DM_CREATED', 'Docker machine created'), ('STATUS_DM_FAILED', 'Docker machine failed'), ('STATUS_SWARM_CREATED', 'Docker swarm created'), ('STATUS_SWARM_FAILED', 'Docker swarm failed')])),
                ('openstack_node_id', models.CharField(max_length=250)),
                ('cluster_id', models.ForeignKey(to='ccloud.Cluster')),
            ],
        ),
        migrations.CreateModel(
            name='Openstack_User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('projectname', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=1, choices=[('A', 'Admin'), ('U', 'User')])),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RequestQueue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'For Create'), ('STATUS_FORMODIFY', 'For Modify'), ('STATUS_FORDELETE', 'For Delete'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified')])),
                ('creation_date', models.DateTimeField(verbose_name='date created')),
                ('last_update_date', models.DateTimeField(verbose_name='date updated')),
                ('created_by', models.CharField(max_length=100)),
                ('container_id', models.ForeignKey(to='ccloud.Container')),
            ],
        ),
    ]
