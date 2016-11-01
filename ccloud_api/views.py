from django.contrib.auth.models import User, Group
from rest_framework import viewsets
import os
import sys
from ccloud_api.serializers import UserSerializer, GroupSerializer, ClusterSerializer
from ccloud_api.permissions import IsOwnerOrReadOnly
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from datetime import datetime
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

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (permissions.IsAdminUser,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ClusterList(APIView):
    permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticated,)
    def get(self, request, format=None):
        clusters=Cluster.objects.filter(user_id=request.user).exclude(status = Cluster.STATUS_DELETED)
        #clusters = Cluster.objects.all()
        serializer = ClusterSerializer(clusters, many=True,context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClusterSerializer(data=request.data)
        if serializer.is_valid():
            cluster_kwargs = serializer.validated_data
            cluster = Cluster(**cluster_kwargs)
            cluster.user_id=request.user
            cluster.status=Cluster.STATUS_FORCREATE
            cluster.no_of_instances=0
            cluster.creation_date=datetime.now()
            cluster.last_update_date=datetime.now()        
            cluster.created_by=request.user.username
            cluster.save()

            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)