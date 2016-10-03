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
from ccloud.models import Container
from ccloud.models import RequestQueue
from io import BytesIO
from docker import Client

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='reqqueue')

def create_container(cname,user,giturl):
    try:
        error = False
        errmsg = ''
        cid=''
        host_port=''
        print('nodeJsBuild start');    
        print('file creation')
        cli = Client(base_url='unix://var/run/docker.sock')
        print('cli creation')
        response = [line for line in cli.build(path=giturl, rm=True, tag=user+'/'+cname)]
        print(response)
        print('cli creation end')
        container = cli.create_container(image=user+'/'+cname)
        print(container)
        ccrres = json.loads(json.dumps(container))
        if 'Id' not in ccrres:
            error = True
            errmsg = 'Container creation failed'
        else:
            print('1')
            cid = ccrres['Id']
            print(cid)
            response = cli.start(container=container.get('Id'))
            print(response)    
            if response != None:            
                error = True
                errmsg = 'Container failed to start'
            else:       
                error = False
                info = cli.inspect_container(container)
                host_port = info['NetworkSettings']['Ports']
        return error,errmsg,cid,host_port
    except:
        return True,'Exception','',''

def remove_container(id):
    cli = Client(base_url='unix://var/run/docker.sock')
    try:
        cli.remove_container(id,force='true')
    except:
        pass

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    rq = RequestQueue.objects.get(id=body)
    c = rq.container_id
    print(c)
    if c.status == Container.STATUS_FORCREATE:
        error,errmsg,id,url = create_container(c.container_name,c.user_id.username,c.git_url)
        if error == False:
            c.status=Container.STATUS_CREATED
            c.devstack_container_id=id
            c.container_url=url
            c.save()
        else:
            c.status=Container.STATUS_FAILED
            c.save()
    elif c.status == Container.STATUS_FORMODIFY:
        remove_container(c.devstack_container_id)
        error,errmsg,id,url = create_container(c.container_name,c.user_id.username,c.git_url)
        print('2222')
        print(id)
        print(url)
        print(error)
        if error == False:
            c.status=Container.STATUS_MODIFIED
            c.devstack_container_id=id
            c.container_url=url
            c.save()
        else:
            c.status=Container.STATUS_FAILED
            c.save()
    elif c.status == Container.STATUS_FORDELETE:
        print(str(c.devstack_container_id))
        remove_container(str(c.devstack_container_id))
        c.delete()
        
channel.basic_consume(callback,
                      queue='reqqueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()