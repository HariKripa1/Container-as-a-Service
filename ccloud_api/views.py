from django.contrib.auth.models import User, Group
from rest_framework import viewsets
import os
import sys
from ccloud_api.serializers import UserSerializer, GroupSerializer, ClusterSerializer, ClusterListSerializer
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
    """
     List all clusters, or create a new cluster.
    """
    permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticated,)
    def get(self, request, format=None):
        clusters=Cluster.objects.filter(user_id=request.user).exclude(status = Cluster.STATUS_DELETED)
        #clusters = Cluster.objects.all()
        serializer = ClusterListSerializer(clusters, many=True,context={'request': request},partial=True)
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
            sendClusterReq(str(cluster.id))
            

            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClusterDetail(APIView):
    """
    Retrieve, update or delete a cluster instance.
    """
    permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Cluster.objects.get(pk=pk)
        except Cluster.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cluster = self.get_object(pk)
        if cluster.user_id == request.user:
            serializer = ClusterListSerializer(cluster)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, format=None):
        cluster = self.get_object(pk)
        if cluster.user_id != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ClusterSerializer(cluster, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            c = Cluster.objects.get(id=pk)
            c.status=Cluster.STATUS_FORMODIFY      
            c.last_update_date=datetime.now()   
            c.save()
            sendClusterReq(str(cluster.id))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cluster = self.get_object(pk)
        if cluster.user_id != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        cluster.status=Cluster.STATUS_FORDELETE           
        cluster.creation_date=datetime.now()
        cluster.last_update_date=datetime.now()        
        cluster.save()#update instead of insert
        sendClusterReq(str(cluster.id))
        return Response(status=status.HTTP_204_NO_CONTENT)


def sendClusterReq(rid):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='clusterQueue')

    channel.basic_publish(exchange='',
                        routing_key='clusterQueue',
                        body=rid)
    print(" [x] Sent request for cluster " + rid)
    connection.close()