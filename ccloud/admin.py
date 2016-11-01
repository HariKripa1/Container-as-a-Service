# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Container, RequestQueue, Cluster, Node, Openstack_User

# Register your models here.
admin.site.register(Container)
admin.site.register(RequestQueue)
admin.site.register(Cluster)
admin.site.register(Node)
admin.site.register(Openstack_User)