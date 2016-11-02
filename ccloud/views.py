
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django import forms
from .forms import NameForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import NameForm
from .forms import AddPage
from .forms import AdminAddPage
from .forms import ModifyPage
from .forms import AddClusterPage
from .forms import AdminAddClusterPage
from .forms import ModifyClusterPage
from .models import Cluster
from .models import Node
from .models import Openstack_User
from .models import Container
from .models import RequestQueue
from django.contrib.auth.models import User
from datetime import datetime
from keystoneauth1.identity import v2
from keystoneauth1 import session
from keystoneclient.v2_0 import client
import pika
import sys
import os
import subprocess
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

def send(rid):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='reqqueue')

    channel.basic_publish(exchange='',
                        routing_key='reqqueue',
                        body=rid)
    print(" [x] Sent 'Hello World!'" + rid)
    connection.close()
    

def sendClusterReq(rid):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='clusterQueue')

    channel.basic_publish(exchange='',
                        routing_key='clusterQueue',
                        body=rid)
    print(" [x] Sent request for cluster " + rid)
    connection.close()
    

def index(request):
    return render(request,'ccloud/index.html')

@login_required
# Create your views here.
def get_name(request):

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/ccloud/thanks/')


    else:
        form = NameForm()

    return render(request, 'ccloud/name.html', {'form': form})


def register(request):
    registered = False

 
    if request.method == 'POST':
        
        user_form = UserForm(data=request.POST)

       
        if user_form.is_valid():
            
            user = user_form.save()
            password = user.password
            
            user.set_password(user.password)
            user.save()
            registered = True
            print str(user.username)
            print str(password)
            #output = subprocess.check_output(['./script/createUser.sh',str(user.username),str(password)])
            #print output
            auth_url='http://172.17.0.1:5000/v2.0'
            auth = v2.Password(username="admin", password="123456",tenant_name="admin", auth_url=auth_url)
            sess = session.Session(auth=auth)
            keystone = client.Client(session=sess)
            keystone.tenants.list() 
            username=user.username
            password=password
            tenant_name="project_"+username
            keystone.tenants.create(tenant_name=tenant_name,description="Default Tenant", enabled=True)
            tenants = keystone.tenants.list()
            my_tenant = [x for x in tenants if x.name==tenant_name][0]
            my_user = keystone.users.create(name=username,password=password,tenant_id=my_tenant.id)
            roles = keystone.roles.list()
            try:
                my_role = [x for x in roles if x.name=='user'][0]
            except:    
                my_role = keystone.roles.create('user')
            if my_role is None:
                my_role = keystone.roles.create('user')
            print my_role    
            keystone.roles.add_user_role(my_user, my_role, my_tenant)
            service = keystone.services.create(name="nova", service_type="compute", description="Nova Compute Service")
            keystone.endpoints.create(region="RegionOne", service_id=service.id, publicurl="http://172.17.0.1:8774/v2/%(tenant_id)s", adminurl="http://172.17.0.1:8774/v2/%(tenant_id)s", internalurl="http://172.17.0.1:8774/v2/%(tenant_id)s")
            openstackuser=Openstack_User(user_id=user,username=str(username),password=str(password),projectname="project_"+str(username),role=Openstack_User.USER)
            openstackuser.save()
        # Invalid form or forms -  or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
            'ccloud/register.html',
            {'user_form': user_form, 'registered': registered})
def user_login(request):
    if request.method=='POST':
    	username=request.POST['username']
    	password=request.POST['password']
    	user=authenticate(username=username,password=password)
    	try:
            auth_url='http://172.17.0.1:5000/v2.0'
            auth = v2.Password(username=username, password=password,tenant_name="project_"+username, auth_url=auth_url)
            sess = session.Session(auth=auth)
            keystone = client.Client(session=sess)
    	except:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    	if user:
    		if user.is_active:
    			login(request,user)    
    			openstackuser = Openstack_User.objects.get(user_id=user.id)
    			request.session['username'] = username
                        request.session['tenant_name'] = "project_"+username
                        return HttpResponseRedirect('/ccloud/user/Home/')
    		else:
    			return HttpResponse("Your CCloud Account is disabled")
    	else:
    	   print "Invalid login details: {0}, {1}".format(username, password)
           return HttpResponse("Invalid login details supplied.")
    else:
        return render(request,'ccloud/login.html',{})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    try:
        del request.session['username']
    except KeyError:
        pass
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/ccloud/')
def thanks(request):
    message = "Successfully submitted"
    context = {'message' : message}
    return render(request, 'ccloud/thanks.html', context)

@login_required
def getMainform(request):        
    username=request.session.get('username')
    user = User.objects.get(username=username)
    container = Container.objects.filter(user_id=user).exclude(status = Container.STATUS_DELETED)
    print(request.session.get('username'))
    #return render(request, 'ccloud/mainPage.html', {'list': zip(containerId,containerNames)} )
    return render(request, 'ccloud/mainPage.html', {'container': container } )

@login_required
def getService(request):
    try:
        cors = request.POST['cors']
    except KeyError:
        cors = "c"
    username=request.session.get('username') 
    user = User.objects.get(username=username)
    if user.is_superuser:
        form = AdminAddPage(request.POST)        
    else:
        form = AddPage(request.POST) 
    print('fasdsas');
    addflg = False;    
    print(request.session.get('username'))       
    cid = ''    
    if form.is_valid():
        # add in db
        print('addd service')
        form.cleaned_data['giturl']            
        message = "add request sent for "+form.cleaned_data['giturl']
        port=form.cleaned_data['port']
        context = {'message' : message}
        addflg = True; 
        try:
            cid = request.POST['cid']
        except KeyError:
            cl=Cluster.objects.get(created_by_admin='Y')[0]
            cid = str(cl.id)
            print 'admin cluster'
            print cid
        print 'clusterid'
        print cid
        try:
            cors = request.POST['cors']
        except KeyError:
            cors = "c"
        cluster = Cluster.objects.get(id=cid)
        if user.is_superuser:
            user = form.cleaned_data['user']            
        else:
            user = User.objects.get(username=username)
        if cors=="c":
            containerorservice=Container.CONTAINER
        else:
            containerorservice=Container.SERVICE
        container=Container(cluster_id=cluster,container_name=form.cleaned_data['containername'],git_url=form.cleaned_data['giturl'],user_id=user,docker_file='Y',application_name='',status=Container.STATUS_FORCREATE,container_url='',devstack_container_id='',creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username,container_or_service=containerorservice,port=port)
        container.save()
        crreq=RequestQueue(container_id = container,status = RequestQueue.STATUS_FORCREATE, creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
        crreq.save()
        send(str(crreq.id))                
        return render(request, 'ccloud/addPage.html', {'form': form,'addflg' : addflg,'cid':cid,'cors':cors})       
    elif "Add" in request.POST:     
        print('add page 2')
        try:
            cid = request.POST['cid']
        except KeyError:
            cid = "1"
        try:
            cors = request.POST['cors']
        except KeyError:
            cors = "c"
        print 'clusterid'
        print cid        
        if user.is_superuser:
            form = AdminAddPage()        
        else:
            form = AddPage()    
        return render(request, 'ccloud/addPage.html', {'form': form,'addflg' : addflg,'cid':cid,'cors':cors})        
    return render(request, 'ccloud/addPage.html', {'form': form,'addflg' : addflg,'cid':cid,'cors':cors})
    
    
    

@login_required
def modifyService(request):    
    form = ModifyPage(request.POST)
    modifyflg = False;
    c_id = '';
    delmodflg = '';
    username=request.session.get('username')    
    if "Modify" in request.POST:                 
        c_id = request.POST.get('cid')
        print 'mod'
        print c_id
        form = ModifyPage()            
        try:
            cors = request.POST.get('cors')
            if cors == None:
                cors="c"
            print cors
        except KeyError:
            cors = "c"
        return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg,'cors':cors})
    elif "Delete" in request.POST:
        c_id = request.POST.get('cid')
        print 'del'
        print c_id
        message = "Deletion request sent for "+c_id
        modifyflg = True;
        user = User.objects.get(username=username)   
        container = Container.objects.get(id=c_id)        
        container.user_id=user        
        container.status=Container.STATUS_FORDELETE           
        container.creation_date=datetime.now()
        container.last_update_date=datetime.now()        
        container.save()#update instead of insert
        crreq=RequestQueue(container_id = container,status = RequestQueue.STATUS_FORDELETE, creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
        crreq.save()
        send(str(crreq.id))
        delmodflg = 'Delete'
        try:
            cors = request.POST.get('cors')
            if cors == None:
                cors="c"
            print cors
        except KeyError:
            cors = "c"
            print cors
        return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg,'delmodflg' : delmodflg,'cors':cors})
    elif form.is_valid():

        # add in db            
        #form.cleaned_data['giturl']   
        c_id = request.POST.get('cid', None)
        #message = "modification request sent for "+form.cleaned_data['giturl']                     
        modifyflg = True;
        user = User.objects.get(username=username)   
        container = Container.objects.get(id=c_id)
        #container.container_name=form.cleaned_data['containername']
        #container.git_url=form.cleaned_data['giturl']
        #container.user_id=user
        #container.docker_file='Y'
        #container.application_name=''
        #container.port=form.cleaned_data['port']

        c_id = request.POST.get('cid', None)
        print c_id
        message = "modification request sent for "
        modifyflg = True;
        user = User.objects.get(username=username)   
        container = Container.objects.get(id=c_id)
>>>>>>> fdfd7b0041cc967eff22bb476dad021597ca3964
        container.scale=form.cleaned_data['scale']
        container.status=Container.STATUS_FORMODIFY        
        container.creation_date=datetime.now()
        container.last_update_date=datetime.now()        
        container.save()#update instead of insert
        crreq=RequestQueue(container_id = container,status = container.status, creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
        crreq.save()
        send(str(crreq.id))
        try:
            cors = request.POST.get('cors')
            if cors == None:
                cors="c"
            print cors
        except KeyError:
            cors = "c"
        delmodflg = 'Modify'
        return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg,'delmodflg' :delmodflg,'cors':cors})
    else:
        message = " error "
        context = {'message' : message, 'modifyflg' : modifyflg}
    return render(request, 'ccloud/thanks.html', context)

@login_required
def getUserHome(request):
    message = "Successfully submitted"
    context = {'message' : message}
    flg='U'
    return render(request, 'ccloud/userHome.html', context)

@login_required
def getAdminHome(request):
    message = "Successfully submitted"
    context = {'message' : message}        
    username=request.session.get('username')
    openstackusers = Openstack_User.objects.filter(role=Openstack_User.USER)
    return render(request, 'ccloud/userHome.html', {'users':openstackusers,'username':username})

@login_required
def getClusterHome(request):        
    username=request.session.get('username')
    user = User.objects.get(username=username)
    print user.username
    print 'dmin'
    print user.is_superuser
    if user.is_superuser:
        cluster = Cluster.objects.filter().exclude(status = Cluster.STATUS_DELETED)        
    else:
        cluster = Cluster.objects.filter(user_id=user).exclude(status = Cluster.STATUS_DELETED)#change to cluster once model is created
    print(request.session.get('username'))    
    return render(request, 'ccloud/clusterHome.html', {'cluster': cluster,'user':user } )

@login_required
def getaddclusterPage(request):
    username=request.session.get('username')
    user = User.objects.get(username=username)
    if user.is_superuser:
        form = AdminAddClusterPage(request.POST)        
    else:
        form = AddClusterPage(request.POST)    
    print('fasdsas');
    addflg = False;  
    message = ''
    if form.is_valid():            
            print('addd cluster')
            form.cleaned_data['clustername']            
            message = "add request sent for "+form.cleaned_data['clustername']
            clustername = form.cleaned_data['clustername']
            username=request.session.get('username')                        
            message = 'Request sent for adding cluster!!'            
            context = {'message' : message}         
            addflg = True;    
            print addflg
            if user.is_superuser:
                user = form.cleaned_data['user']            
            else:
                user = User.objects.get(username=username)
            print user
            cluster=Cluster(cluster_name=form.cleaned_data['clustername'],user_id=user,status=Cluster.STATUS_FORCREATE,no_of_instances=0,requested_no_of_instance=form.cleaned_data['noOfNodes'],creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
            cluster.save()
            sendClusterReq(str(cluster.id))
            return render(request, 'ccloud/addclusterPage.html', {'form': form,'addflg' : addflg,'message':message})
    else:
        print('add page 2')
        if user.is_superuser:
            form = AdminAddClusterPage()        
        else:
            form = AddClusterPage()               
    return render(request, 'ccloud/addclusterPage.html', {'form': form,'addflg' : addflg,'message':message})


@login_required
def getmodifyclusterPage(request):
    form =  ModifyClusterPage(request.POST)
    print('fasdsas');
    addflg = False;    
    username=request.session.get('username')
    cid = '';
    user = User.objects.get(username=username)    
    c='';
    modorview=False;
    message=''
    if "Redeploy" in request.POST or "View" in request.POST :
        print('ttpe1')
        if "Redeploy" in request.POST :
            modorview=True
        else:
            modorview=False        
        print('add page 2')        
        cid = request.POST['cid']
        print(cid)
        cluster= Cluster.objects.get(id=cid)                    
        node = Node.objects.filter(cluster_id=cluster).exclude(status = Cluster.STATUS_DELETED)#change to cluster once model is created
        service = Container.objects.filter(cluster_id=cluster)
        form = ModifyClusterPage()
        return render(request, 'ccloud/modifyclusterPage.html', {'form': form,'addflg' : addflg,'cid':cid,'modorview':modorview,'message':message,'node':node,'service':service})
    elif "Delete" in request.POST:       
        cid = request.POST.get('cid', None)
        print(cid)        
        addflg = True; 
        message = "Delete request sent for "+cid
        cluster = Cluster.objects.get(id=cid)                      
        cluster.status=Cluster.STATUS_FORDELETE           
        cluster.creation_date=datetime.now()
        cluster.last_update_date=datetime.now()        
        cluster.save()#update instead of insert
        sendClusterReq(str(cluster.id))
        return render(request, 'ccloud/modifyclusterPage.html', {'form': form,'addflg' : addflg,'cid':cid,'modorview':modorview,'message':message})
    elif form.is_valid():
            # add in db
            print('addd cluster')            
            cid = request.POST.get('cid', None)
            print(cid)
            message = "Modify request sent for "+cid
            print(message)
            print(cid)
            context = {'message' : cid}
            addflg = True; 
            user = User.objects.get(username=username)    
            cluster= Cluster.objects.get(id=cid)                             
            cluster.status=Cluster.STATUS_FORMODIFY        
            cluster.requested_no_of_instance = form.cleaned_data['noOfNodes']        
            cluster.creation_date=datetime.now()
            cluster.last_update_date=datetime.now()        
            cluster.save()           
            node = Node.objects.filter(cluster_id=cluster).exclude(status = Cluster.STATUS_DELETED)#change to cluster once model is created
            sendClusterReq(str(cluster.id))
            return render(request, 'ccloud/modifyclusterPage.html', {'form': form,'addflg' : addflg,'cid':cid,'modorview':modorview,'message':message,'node': node})
    return render(request, 'ccloud/modifyclusterPage.html', {'form': form,'addflg' : addflg,'cid':cid,'modorview':modorview,'message':message})
