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
        print openstackuser.username
        print openstackuser.password
        print openstackuser.projectname
        print c.requested_no_of_instance
        cluster_count = Cluster.objects.filter(user_id=c.user_id).count()
        print cluster_count
        if cluster_count > 1:
            output = subprocess.check_output(['./script/buildSwarmNext.sh',str(openstackuser.username),str(openstackuser.password),str(openstackuser.projectname),str(c.requested_no_of_instance),str(c.id)])
            print output
        else:    
            output = subprocess.check_output(['./script/buildSwarm.sh',str(openstackuser.username),str(openstackuser.password),str(openstackuser.projectname),str(c.requested_no_of_instance),str(c.id)])
            print output
        nodes=output.split('\n')
        regex = re.compile('Machine-Information:.*')
        j = 0
        for i in nodes:
            n = regex.match(i)
            if n:
                data=n.group()
                data=data.split(':')
                name=data[1]
                ip=data[2]
                instance_id=data[3]
                print ip
                print name
                print instance_id
                if j==0:
                    master='Y'
                    c.master_ip=ip
                    c.master_name=name
                    c.save()
                else:
                    master='N'
                j=j+1    
                node=Node(cluster_id=c,machine_ip=ip,machine_name=name,master=master,status=Node.STATUS_CREATED,openstack_node_id=instance_id)
                node.save()        
                c.no_of_instances = c.requested_no_of_instance
                c.save()
        return error,errmsg
    except Exception as inst:
	print inst.args
        return True,'Exception'

def modify_cluster(c):
    error = False
    errmsg= ''    
    try:
        print 'modify cluster'
        print c.user_id
        openstackuser = Openstack_User.objects.get(user_id=c.user_id)
        user = c.user_id
        print openstackuser.username
        print openstackuser.password
        print openstackuser.projectname
        print c.requested_no_of_instance
        print c.no_of_instances        
        if c.requested_no_of_instance > c.no_of_instances:   
            print 'if'
            output = subprocess.check_output(['./script/modifySwarm.sh',str(openstackuser.username),str(openstackuser.password),str(openstackuser.projectname),str(c.no_of_instances),str(c.requested_no_of_instance),str(c.id)])
            print output     
            nodes=output.split('\n')
            regex = re.compile('Machine-Information:.*')        
            for i in nodes:
                n = regex.match(i)
                if n:
                    data=n.group()
                    data=data.split(':')
                    name=data[1]
                    ip=data[2]
                    instance_id=data[3]
                    master='N'
                    print name
                    print ip
                    print instance_id
                    node=Node(cluster_id=c,machine_ip=ip,machine_name=name,master=master,status=Node.STATUS_CREATED,openstack_node_id=instance_id)
                    node.save()        
                    c.no_of_instances = c.requested_no_of_instance
                    c.save()
            return error,errmsg        
        else:
            print 'else'
            diff = int(c.no_of_instances) - int(c.requested_no_of_instance)
            node = Node.objects.filter(cluster_id=c.id).order_by('-machine_ip')[:diff]
            for n in node:
                print n.machine_name
                output = subprocess.check_output(['./script/deleteSwarmnode.sh',str(openstackuser.username),str(openstackuser.password),str(openstackuser.projectname),str(n.machine_name)])
                print output 
                n.delete()
            c.no_of_instances = c.requested_no_of_instance
            c.save()    
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
        node = Node.objects.filter(cluster_id=c.id).order_by('-machine_ip')
        for n in node:
            print n.machine_name
            output = subprocess.check_output(['./script/deleteSwarmnode.sh',str(user.username),str(openstackuser.password),str(openstackuser.projectname),str(n.machine_name)])
            print output  
            n.delete() 
            print 'deleted'
        return error,errmsg
    except Exception as inst:
       print inst.args
       return True,'Exception' 
        
    
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    c = Cluster.objects.get(id=body)
    print(c.id)    
    print c.status
    if c.status == Cluster.STATUS_FORCREATE:
        print 'create'
        error,errmsg = create_cluster(c)
        if error == False:
            c.status=Cluster.STATUS_NODE_COMPLETE            
            c.save()            
            senddockerCreate(str(c.id))            
        else:
            c.status=Cluster.STATUS_NODE_FAILED
            c.save()
    elif c.status == Cluster.STATUS_FORMODIFY:
        print 'modify'
        error,errmsg = modify_cluster(c)
        if error == False:
            c.status=Cluster.STATUS_NODE_COMPLETE            
            c.save()      
            senddockerCreate(str(c.id))            
        else:
            c.status=Cluster.STATUS_NODE_FAILED
            c.save()
    elif c.status == Cluster.STATUS_FORDELETE:
        print 'delete'
        error,errmsg = remove_cluster(c)
        if error == False:
            c.status=Cluster.STATUS_DELETED            
            c.save()            
        else:
            c.status=Cluster.STATUS_DELETE_FAILED
            c.save()
        
channel.basic_consume(callback,
                      queue='clusterQueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
