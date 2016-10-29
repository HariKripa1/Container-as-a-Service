import pika
import sys
import os
import json
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
from ccloud.models import RequestQueue
from ccloud.models import Openstack_User
from ccloud.models import User
from ccloud.models import Node
from io import BytesIO
from docker import Client
import docker.tls as tls
import subprocess
import re

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='clusterQueue')

def senddockerCreate(rid):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='dmQueue')

    channel.basic_publish(exchange='',
                        routing_key='dmQueue',
                        body=rid)
    print(" [x] Sent request for cluster " + rid)
    connection.close()

def create_cluster(c):
    error = False
    errmsg= ''    
    try:
        print c.user_id
        openstackuser = Openstack_User.objects.get(user_id=c.user_id)
        user = c.user_id
        print user.username
        print user.password
        print openstackuser.projectname
        print c.requested_no_of_instance
        output = subprocess.check_output(['./script/buildSwarm.sh',str(user.username),str(user.password),str(openstackuser.projectname),str(c.requested_no_of_instance)])
        print output
        nodes=output.split('\n')
        j = 0
        for i in nodes:
            n=re.match('Machine-Information:(.*),(.*)',i)
            if n:
                name=n.group(1)
                ip=n.group(2)
                if j==0:
                    master='Y'
                    c.master_ip=ip
                    c.save()
                else:
                    master='N'
                j=j+1    
                node=Node(cluster_id=c,machine_ip=ip,machine_name=name,master=master,status=Node.STATUS_CREATED)
                node.save()        
        return error,errmsg
    except Exception as inst:
	print inst.args
        return True,'Exception'

def modify_cluster(c):
    error = False
    errmsg= ''    
    try:
        print c.user_id
        openstackuser = Openstack_User.objects.get(user_id=c.user_id)
        user = c.user_id
        print user.username
        print user.password
        print openstackuser.projectname
        print c.requested_no_of_instance
        #call modify script
        #output = subprocess.check_output([user.username,user.password,openstackuser.projectname,c.requested_no_of_instance])
        #print output         
        return error,errmsg
    except Exception as inst:
	print inst.args
        return True,'Exception'
    
def remove_cluster(c):
    error = False
    errmsg= ''
    try:
        print c.user_id
        openstackuser = Openstack_User.objects.get(user_id=c.user_id)
        user = c.user_id
        print user.username
        print user.password
        print openstackuser.projectname
        print c.requested_no_of_instance
        #call delete script
        #output = subprocess.check_output([user.username,user.password,openstackuser.projectname,c.requested_no_of_instance])
        #print output               
        return error,errmsg
    except Exception as inst:
       print inst.args
       return True,'Exception' 
        
    
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    c = Cluster.objects.get(id=body)    
    print(c.id)
    if c.status == Cluster.STATUS_FORCREATE:
        error,errmsg = create_cluster(c)
        if error == False:
            c.status=Cluster.STATUS_NODE_COMPLETE            
            c.save()            
            senddockerCreate(str(c.id))            
        else:
            c.status=Cluster.STATUS_NODE_FAILED
            c.save()
    elif c.status == Cluster.STATUS_FORMODIFY:
        error,errmsg = modify_cluster(c)
        if error == False:
            c.status=Cluster.STATUS_NODE_COMPLETE            
            c.save()            
        else:
            c.status=Cluster.STATUS_NODE_FAILED
            c.save()
    elif c.status == Cluster.STATUS_FORDELETE:
        error,errmsg = delete_cluster(c)
        if error == False:
            c.status=Cluster.STATUS_DELETED            
            c.save()
            #delete from Node model
        else:
            c.status=Cluster.STATUS_DELETE_FAILED
            c.save()
        
channel.basic_consume(callback,
                      queue='clusterQueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()