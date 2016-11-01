from django.contrib.auth.models import User, Group
from rest_framework import serializers
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
from ccloud.models import Cluster


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ClusterListSerializer(serializers.HyperlinkedModelSerializer):
	user = serializers.ReadOnlyField(source='user_id.username')
	class Meta:
		model = Cluster
		fields = ('id','cluster_name', 'requested_no_of_instance','user','status','no_of_instances')


class ClusterSerializer(serializers.HyperlinkedModelSerializer):
	#user = serializers.ReadOnlyField(source='user_id.username')
	class Meta:
		model = Cluster
		fields = ('cluster_name', 'requested_no_of_instance')
