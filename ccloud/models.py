# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cluster(models.Model):
    STATUS_FORCREATE = 'STATUS_FORCREATE'
    STATUS_FORMODIFY = 'STATUS_FORMODIFY'
    STATUS_FORDELETE = 'STATUS_FORDELETE'
    STATUS_CREATED = 'STATUS_CREATED'
    STATUS_DELETED = 'STATUS_DELETED'
    STATUS_MODIFIED = 'STATUS_MODIFIED'
    STATUS_CREATE_FAILED = 'STATUS_CREATE_FAILED'
    STATUS_MODIFY_FAILED = 'STATUS_MODIFY_FAILED'
    STATUS_DELETE_FAILED = 'STATUS_DELETE_FAILED'
    STATUS_NODE_COMPLETE = 'STATUS_NODE_COMPLETE'    
    STATUS_NODE_FAILED = 'STATUS_NODE_FAILED'
    STATUS_DM_CREATED = 'STATUS_DM_CREATED'
    STATUS_DM_FAILED = 'STATUS_DM_FAILED'
    STATUS_SWARM_CREATED = 'STATUS_SWARM_CREATED'
    STATUS_SWARM_FAILED = 'STATUS_SWARM_FAILED'
    STATUS_CHOICES = (
        (STATUS_FORCREATE,'Creation in progress'),
        (STATUS_NODE_COMPLETE,'Creation in progress'),
        (STATUS_FORMODIFY,'Modification in progress'),
        (STATUS_NODE_FAILED,'Deletion in progress'),
        (STATUS_FORDELETE,'Deletion in progress'),
        (STATUS_CREATED,'Created'),
        (STATUS_DELETED,'Delete'),
        (STATUS_MODIFIED,'Modified'),
        (STATUS_CREATE_FAILED,'Clutser creation failed'),
        (STATUS_MODIFY_FAILED,'Cluster redeployment failed'),
        (STATUS_DELETE_FAILED,'Cluster deletion failed'),
        (STATUS_DM_CREATED,'Docker machine created. Wait for swarm creation'),
        (STATUS_DM_FAILED,'Docker machine failed'),
        (STATUS_SWARM_CREATED,'Docker swarm created'),
        (STATUS_SWARM_FAILED,'Docker swarm failed')
    )
    ADMIN = 'Y'
    USER = 'N'
    LOOKUP_CHOICES = (
        (ADMIN,'Admin'),
        (USER,'User')
    )
    cluster_name = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES)
    no_of_instances = models.IntegerField()
    requested_no_of_instance = models.IntegerField()
    master_ip = models.CharField(max_length=200)
    master_name=models.CharField(max_length=200)
    token_id = models.CharField(max_length=500)
    creation_date = models.DateTimeField('date created')
    last_update_date = models.DateTimeField('date updated')
    created_by=models.CharField(max_length=100)
    created_by_admin=models.CharField(max_length=1,choices=LOOKUP_CHOICES)
    def __str__(self):
        return self.cluster_name

class Node(models.Model):
    MASTER_Y = 'Y'
    MASTER_N = 'N'
    MASTER_CHOICES = (
        (MASTER_Y,'Master'),
        (MASTER_N,'Worker')
    )
    STATUS_FORCREATE = 'STATUS_FORCREATE'
    STATUS_FORMODIFY = 'STATUS_FORMODIFY'
    STATUS_FORDELETE = 'STATUS_FORDELETE'
    STATUS_CREATED = 'STATUS_CREATED'
    STATUS_DELETED = 'STATUS_DELETED'
    STATUS_MODIFIED = 'STATUS_MODIFIED'
    STATUS_CREATE_FAILED = 'STATUS_CREATE_FAILED'
    STATUS_MODIFY_FAILED = 'STATUS_MODIFY_FAILED'
    STATUS_DELETE_FAILED = 'STATUS_DELETE_FAILED'
    STATUS_DM_CREATED = 'STATUS_DM_CREATED'
    STATUS_DM_FAILED = 'STATUS_DM_FAILED'
    STATUS_SWARM_CREATED = 'STATUS_SWARM_CREATED'
    STATUS_SWARM_FAILED = 'STATUS_SWARM_FAILED'
    STATUS_CHOICES = (
        (STATUS_FORCREATE,'Creation in progress'),
        (STATUS_FORMODIFY,'Modification in progress'),
        (STATUS_FORDELETE,'Deletion in progress'),
        (STATUS_CREATED,'Created'),
        (STATUS_DELETED,'Delete'),
        (STATUS_MODIFIED,'Modified'),
        (STATUS_CREATE_FAILED,'Node creation failed'),
        (STATUS_MODIFY_FAILED,'Node redeployment failed'),
        (STATUS_DELETE_FAILED,'Node deletion failed'),
        (STATUS_DM_CREATED,'Docker machine created'),
        (STATUS_DM_FAILED,'Docker machine failed'),
        (STATUS_SWARM_CREATED,'Docker swarm created'),
        (STATUS_SWARM_FAILED,'Docker swarm failed')
    )
    cluster_id = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    machine_ip = models.CharField(max_length=200)
    master=models.CharField(max_length=1,choices=MASTER_CHOICES)
    machine_name=models.CharField(max_length=200)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES)
    openstack_node_id=models.CharField(max_length=250,unique=True)
    def __str__(self):
        return self.cluster_id
    
class Openstack_User(models.Model):
    ADMIN = 'A'
    USER = 'U'
    LOOKUP_CHOICES = (
        (ADMIN,'Admin'),
        (USER,'User')
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)    
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200) 
    projectname = models.CharField(max_length=200)
    role = models.CharField(max_length=1,choices=LOOKUP_CHOICES)
    def __str__(self):
        return str(self.user_id)
    
class Container(models.Model):
    APPLICATION_NODE_JS = 'APPLICATION_NODE_JS'
    APPLICATION_CHOICES = (
        (APPLICATION_NODE_JS,'Node JS'),
    )
    LOOKUP_Y = 'Y'
    LOOKUP_N = 'N'
    LOOKUP_CHOICES = (
        (LOOKUP_Y,'Yes'),
        (LOOKUP_N,'No')
    )
    CONTAINER = 'C'
    SERVICE = 'S'
    CORS_CHOICES = (
        (CONTAINER,'Container'),
        (SERVICE,'Service')
    )
    STATUS_FORCREATE = 'STATUS_FORCREATE'
    STATUS_FORMODIFY = 'STATUS_FORMODIFY'
    STATUS_FORDELETE = 'STATUS_FORDELETE'
    STATUS_CREATED = 'STATUS_CREATED'
    STATUS_DELETED = 'STATUS_DELETED'
    STATUS_MODIFIED = 'STATUS_MODIFIED'
    STATUS_CREATE_FAILED = 'STATUS_CREATE_FAILED'
    STATUS_MODIFY_FAILED = 'STATUS_MODIFY_FAILED'
    STATUS_DELETE_FAILED = 'STATUS_DELETE_FAILED'
    STATUS_CHOICES = (
        (STATUS_FORCREATE,'Creation in progress'),
        (STATUS_FORMODIFY,'Modification in progress'),
        (STATUS_FORDELETE,'Deletion in progress'),
        (STATUS_CREATED,'Created'),
        (STATUS_DELETED,'Delete'),
        (STATUS_MODIFIED,'Modified'),
        (STATUS_CREATE_FAILED,'Container creation failed'),
        (STATUS_MODIFY_FAILED,'Container redeployment failed'),
        (STATUS_DELETE_FAILED,'Container deletion failed')
    )
    cluster_id = models.ForeignKey(Cluster, related_name='containers', on_delete=models.CASCADE)
    container_name = models.CharField(max_length=200)
    git_url = models.CharField(max_length=1000)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    docker_file=models.CharField(max_length=1,choices=LOOKUP_CHOICES)
    application_name=models.CharField(max_length=100,choices=APPLICATION_CHOICES)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES)
    container_url=models.CharField(max_length=1000)
    devstack_container_id=models.CharField(max_length=1000)
    creation_date = models.DateTimeField('date created')
    last_update_date = models.DateTimeField('date updated')
    created_by=models.CharField(max_length=100)
    container_or_service = models.CharField(max_length=100,choices=CORS_CHOICES)
    port=models.CharField(max_length=100)
    scale=models.CharField(max_length=100)
    def __str__(self):
        return self.container_name


class RequestQueue(models.Model):
    STATUS_FORCREATE = 'STATUS_FORCREATE'
    STATUS_FORMODIFY = 'STATUS_FORMODIFY'
    STATUS_FORDELETE = 'STATUS_FORDELETE'
    STATUS_CREATED = 'STATUS_CREATED'
    STATUS_DELETED = 'STATUS_DELETED'
    STATUS_MODIFIED = 'STATUS_MODIFIED'
    STATUS_CHOICES = (
        (STATUS_FORCREATE,'For Create'),
        (STATUS_FORMODIFY,'For Modify'),
        (STATUS_FORDELETE,'For Delete'),
        (STATUS_CREATED,'Created'),
        (STATUS_DELETED,'Delete'),
        (STATUS_MODIFIED,'Modified')
    )
    container_id = models.ForeignKey(Container, on_delete=models.CASCADE)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES)
    creation_date = models.DateTimeField('date created')
    last_update_date = models.DateTimeField('date updated')
    created_by=models.CharField(max_length=100)
    def __str__(self):
        return str(self.container_id)

class Price(models.Model):
    
    instance_id = models.ForeignKey(Node, to_field='openstack_node_id', db_column='openstack_node_id', on_delete=models.CASCADE)
    price=models.FloatField()
    def __str__(self):
        return str(self.id)

