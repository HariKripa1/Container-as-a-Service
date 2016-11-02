from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^name$', views.get_name, name='get_name'),
    url(r'^register$', views.register, name='register'),
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.user_login, name='login'),
    url(r'^logout$', views.user_logout, name='logout'),
    url(r'^your-name/$', views.get_name, name='get_name'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^user/service/main/$', views.getMainform, name='getMainform'),
    url(r'^user/Home/$', views.getUserHome, name='userHome'),
    url(r'^admin/Home/$', views.getUserHome, name='getUserHome'),
    url(r'^admin/user/home$', views.getUserHome, name='getUserHome'),
    url(r'^admin/cluster/add/$', views.getaddclusterPage, name='addclusterPage'),
    url(r'^user/cluster/home/$', views.getClusterHome, name='clusterHome'),
    url(r'^user/cluster/add/$', views.getaddclusterPage, name='addclusterPage'),
    url(r'^user/cluster/modify/$', views.getmodifyclusterPage, name='modifyclusterPage'),
    url(r'^user/service/add/$', views.getService, name='getService'),
    url(r'^user/service/modify/$', views.modifyService, name='modifyService'),     
]
