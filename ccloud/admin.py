# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Container, RequestQueue

# Register your models here.
admin.site.register(Container)
admin.site.register(RequestQueue)
