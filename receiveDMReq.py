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

def sendSwarm(rid):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='swarmQueue')

    channel.basic_publish(exchange='',
                        routing_key='swarmQueue',
                        body=rid)
    print(" [x] Sent request for cluster " + rid)
    connection.close()

def create_dm(c,n):
    error = False
    errmsg= ''    
    try:
        print c.user_id
        openstackuser = Openstack_User.objects.get(user_id=c.user_id)
        user = c.user_id
        print openstackuser.username
        print openstackuser.password
        print openstackuser.projectname        
        print n.machine_ip
        print n.machine_name
        output = subprocess.check_output(['./script/createDockerMachine.sh',str(openstackuser.username),str(openstackuser.password),str(openstackuser.projectname),str(n.machine_ip),str(n.machine_name)])
        print output            
        return error,errmsg
    except Exception as inst:
	print inst.args
        return True,'Exception'

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    c = Cluster.objects.get(id=body)    
    print(c.id)
    errflg=False
    #get all node of the cluster
    node = Node.objects.filter(cluster_id=c.id)
    for n in node:       
        error,errmsg = create_dm(c,n)
        if error == False:
            c.status=Cluster.STATUS_DM_CREATED            
            c.save()                                 
            errflg=False 
        else:
            c.status=Cluster.STATUS_DM_FAILED
            c.save()            
            errflg=True
    if errflg == False:
        sendSwarm(str(c.id))          
channel.basic_consume(callback,
                      queue='dmQueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()