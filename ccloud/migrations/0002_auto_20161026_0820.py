# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ccloud', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cluster_name', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Clutser creation failed'), ('STATUS_MODIFY_FAILED', 'Cluster redeployment failed'), ('STATUS_DELETE_FAILED', 'Cluster deletion failed')])),
                ('no_of_instances', models.IntegerField()),
                ('requested_no_of_instance', models.IntegerField()),
                ('master_ip', models.CharField(max_length=200)),
                ('token_id', models.CharField(max_length=500)),
                ('creation_date', models.DateTimeField(verbose_name='date created')),
                ('last_update_date', models.DateTimeField(verbose_name='date updated')),
                ('created_by', models.CharField(max_length=100)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('machine_ip', models.CharField(max_length=200)),
                ('master', models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')])),
                ('machine_name', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Node creation failed'), ('STATUS_MODIFY_FAILED', 'Node redeployment failed'), ('STATUS_DELETE_FAILED', 'Node deletion failed')])),
                ('cluster_id', models.ForeignKey(to='ccloud.Cluster')),
            ],
        ),
        migrations.CreateModel(
            name='openstack_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projectname', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=1, choices=[('A', 'Admin'), ('U', 'User')])),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='container',
            name='status',
            field=models.CharField(max_length=100, choices=[('STATUS_FORCREATE', 'Creation in progress'), ('STATUS_FORMODIFY', 'Modification in progress'), ('STATUS_FORDELETE', 'Deletion in progress'), ('STATUS_CREATED', 'Created'), ('STATUS_DELETED', 'Delete'), ('STATUS_MODIFIED', 'Modified'), ('STATUS_CREATE_FAILED', 'Container creation failed'), ('STATUS_MODIFY_FAILED', 'Container redeployment failed'), ('STATUS_DELETE_FAILED', 'Container deletion failed')]),
        ),
    ]
