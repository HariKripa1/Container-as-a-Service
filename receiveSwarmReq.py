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
import swarm
import json
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='swarmQueue')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    c = Cluster.objects.get(id=body)    
    print(c.id)    
    print 'cluster'
    node = Node.objects.filter(cluster_id=c.id)
    d=swarm.DockerSwarm()
    for n in node:   
        if n.status == Node.STATUS_DM_CREATED:
            print n.machine_ip
            print n.machine_name
            if n.master == 'Y':
                d.init_manager('dm-'+n.machine_name,n.machine_ip)
                print 'init manager'
                print n.machine_ip
                print n.machine_name
                #response = json.loads(res)
                #print response
                n.status=Node.STATUS_SWARM_CREATED
                n.save()
            else:
                d.join_swarm('dm-'+n.machine_name,n.machine_ip,c.master_ip,c.token_id)            
                print 'join swarm'
                print n.machine_ip
                print n.machine_name
                n.status=Node.STATUS_SWARM_CREATED
                n.save()
    c.status=Cluster.STATUS_SWARM_CREATED
    c.save()
    
channel.basic_consume(callback,
                      queue='swarmQueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()