"""Caas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
import os
import sys
##get project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from django.core.wsgi import get_wsgi_application
##get project parent directory and add to python path using sys.path.append
SYS_PATH = os.path.dirname(BASE_DIR)
print SYS_PATH
if SYS_PATH not in sys.path:
    sys.path.append(SYS_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'Caas.settings'
application = get_wsgi_application()
from ccloud_api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
#router.register(r'clusters',views)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ccloud/',include('ccloud.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^ccloud-api/clusters/$', views.ClusterList.as_view()),
    url(r'^ccloud-api/clusters/(?P<pk>[0-9]+)/$', views.ClusterDetail.as_view()),
]
#urlpatterns = format_suffix_patterns(urlpatterns)
