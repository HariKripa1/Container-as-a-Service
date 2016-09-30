# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Containers(models.Model):
    Container_name = models.CharField(max_length=200)
    Creation_date = models.DateTimeField('date created')
    Update_date = models.DateTimeField('date updated')
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.Container_name


class RequestQueue(models.Model):
    container = models.ForeignKey(Containers, on_delete=models.CASCADE)
    operation = models.CharField(max_length=200)
    def __str__(self):
        return self.container

