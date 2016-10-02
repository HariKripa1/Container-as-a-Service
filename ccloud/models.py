# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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

