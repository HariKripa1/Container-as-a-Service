import pika
import sys
import os
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
    print('nodeJsBuild start');    
    print('file creation')
    cli = Client(base_url='unix://var/run/docker.sock')
    print('cli creation')
    response = [line for line in cli.build(path=giturl, rm=True, tag=user+'/'+cname)]
    response
    print('cli creation end')
    container = cli.create_container(image=user+'/'+cname, ports=[(8080, 'tcp')],host_config=cli.create_host_config(port_bindings={'8080/tcp': 49160}))
    print(container)
    response = cli.start(container=container.get('Id'))
    print(response)    
    return

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    rq = RequestQueue.objects.get(id=body)
    c = rq.container_id
    print(c)
    if c.status == Container.STATUS_FORCREATE:
        create_container(c.container_name,c.user_id.username,c.git_url)
    elif c.status == Container.STATUS_FORMODIFY:
        create_container(c.container_name,c.user_id.username,c.git_url)
    elif c.status == Container.STATUS_FORDELETE:
        create_container(c.container_name,c.user_id.username,c.git_url)
        
channel.basic_consume(callback,
                      queue='reqqueue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()