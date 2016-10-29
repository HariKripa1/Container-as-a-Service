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
from .forms import ModifyPage
from .forms import AddClusterPage
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
    return HttpResponseRedirect('/ccloud/thanks/')

def sendClusterReq(rid):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='clusterQueue')

    channel.basic_publish(exchange='',
                        routing_key='clusterQueue',
                        body=rid)
    print(" [x] Sent request for cluster " + rid)
    connection.close()
    return HttpResponseRedirect('/ccloud/thanks/')

def index(request):
    return render(request,'ccloud/index.html')

@login_required
# Create your views here.
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/ccloud/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'ccloud/name.html', {'form': form})


def register(request):
    # Like before, get the request's context.
    #context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            password = user.password
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            registered = True
            print str(user.username)
            print str(password)
            #output = subprocess.check_output(['./script/createUser.sh',str(user.username),str(password)])
            #print output
            auth_url='http://10.0.2.15:5000/v2.0'
            auth = v2.Password(username="admin", password="password",tenant_name="admin", auth_url=auth_url)
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
            keystone.endpoints.create(region="RegionOne", service_id=service.id, publicurl="http://10.0.2.15:8774/v2/%(tenant_id)s", adminurl="http://10.0.2.15:8774/v2/%(tenant_id)s", internalurl="http://10.0.2.15:8774/v2/%(tenant_id)s")
            openstackuser=Openstack_User(user_id=user,username=str(username),password=str(password),projectname="project_"+str(username),role="user")
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
            auth_url='http://10.0.2.15:5000/v2.0'
            auth = v2.Password(username=username, password=password,tenant_name="project_"+username, auth_url=auth_url)
            sess = session.Session(auth=auth)
            keystone = client.Client(session=sess)
    	except:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    	if user:
    		if user.is_active:
    			login(request,user)    			
    			request.session['username'] = username
    			request.session['tenant_name'] = "project_"+username
    			return HttpResponseRedirect('/ccloud/userHome/')
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
def getAddPage(request):
    form = AddPage(request.POST)
    print('fasdsas');
    addflg = False;    
    print(request.session.get('username'))   
    username=request.session.get('username')
    if form.is_valid():
            # add in db
            print('addd page')
            form.cleaned_data['giturl']            
            message = "add request sent for "+form.cleaned_data['giturl']
            context = {'message' : message}
            addflg = True; 
            user = User.objects.get(username=username)
            container=Container(container_name=form.cleaned_data['containername'],git_url=form.cleaned_data['giturl'],user_id=user,docker_file=form.cleaned_data['dockerfilereq'],application_name=form.cleaned_data['application'],status=Container.STATUS_FORCREATE,container_url='',devstack_container_id='',creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
            container.save()
            crreq=RequestQueue(container_id = container,status = RequestQueue.STATUS_FORCREATE, creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
            crreq.save()
            send(str(crreq.id))
            return render(request, 'ccloud/addPage.html', {'form': form,'addflg' : addflg})
    else:
        print('add page 2')
        form = AddPage()                
    return render(request, 'ccloud/addPage.html', {'form': form,'addflg' : addflg})

@login_required
def getModifyPage(request):    
    form = ModifyPage(request.POST)
    modifyflg = False;
    c_id = '';
    delmodflg = '';
    username=request.session.get('username')    
    if "Redeploy" in request.POST:         
        c_id = request.POST['cid']        
        form = ModifyPage()            
        return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg})
    elif "Delete" in request.POST:
        c_id = request.POST['cid']
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
        return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg,'delmodflg' : delmodflg})
    elif form.is_valid():
        # add in db            
        form.cleaned_data['giturl']   
        c_id = request.POST.get('cid', None)
        message = "modification request sent for "+form.cleaned_data['giturl']                     
        modifyflg = True;
        user = User.objects.get(username=username)   
        container = Container.objects.get(id=c_id)
        container.container_name=form.cleaned_data['containername']
        container.git_url=form.cleaned_data['giturl']
        container.user_id=user
        container.docker_file=form.cleaned_data['dockerfilereq']
        container.application_name=form.cleaned_data['application']
        container.status=Container.STATUS_FORMODIFY        
        container.creation_date=datetime.now()
        container.last_update_date=datetime.now()        
        container.save()#update instead of insert
        crreq=RequestQueue(container_id = container,status = container.status, creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
        crreq.save()
        send(str(crreq.id))
        delmodflg = 'Modify'
        return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg,'delmodflg' : delmodflg})
    else:
        message = " error "
        context = {'message' : message, 'modifyflg' : modifyflg}
    return render(request, 'ccloud/thanks.html', context)

@login_required
def getUserHome(request):
    message = "Successfully submitted"
    context = {'message' : message}
    return render(request, 'ccloud/userHome.html', context)

@login_required
def getClusterHome(request):        
    username=request.session.get('username')
    user = User.objects.get(username=username)
    cluster = Cluster.objects.filter(user_id=user).exclude(status = Cluster.STATUS_DELETED)#change to cluster once model is created
    print(request.session.get('username'))
    #return render(request, 'ccloud/mainPage.html', {'list': zip(containerId,containerNames)} )
    return render(request, 'ccloud/clusterHome.html', {'cluster': cluster } )

@login_required
def getaddclusterPage(request):
    form = AddClusterPage(request.POST)
    print('fasdsas');
    addflg = False;  
    message = ''
    if form.is_valid():
            # add in db
            print('addd cluster')
            form.cleaned_data['clustername']            
            message = "add request sent for "+form.cleaned_data['clustername']
            clustername = form.cleaned_data['clustername']
            username=request.session.get('username')            
            if Cluster.objects.filter(cluster_name=clustername).exists():
                message = 'Cluster name already in use'
                return render(request, 'ccloud/addclusterPage.html', {'form': form,'addflg' : addflg,'message':message})
            message = 'Request sent for adding cluster!!'            
            context = {'message' : message}         
            addflg = True;    
            user = User.objects.get(username=username)           
            cluster=Cluster(cluster_name=form.cleaned_data['clustername'],user_id=user,status=Cluster.STATUS_FORCREATE,no_of_instances=0,requested_no_of_instance=form.cleaned_data['noOfNodes'],creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
            cluster.save()
            sendClusterReq(str(cluster.id))
            return render(request, 'ccloud/addclusterPage.html', {'form': form,'addflg' : addflg,'message':message})
    else:
        print('add page 2')
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
        form = ModifyClusterPage()
        return render(request, 'ccloud/modifyclusterPage.html', {'form': form,'addflg' : addflg,'cid':cid,'modorview':modorview,'message':message})
    elif "Delete" in request.POST:       
        cid = request.POST.get('cid', None)
        print(cid)        
        addflg = True; 
        message = "Delete request sent for "+cid
        cluster = Cluster.objects.get(id=cid)        
        cluster.user_id=user        
        cluster.status=Container.STATUS_FORDELETE           
        cluster.creation_date=datetime.now()
        cluster.last_update_date=datetime.now()        
        cluster.save()#update instead of insert
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
            cluster.user_id=user       
            cluster.status=Container.STATUS_FORMODIFY        
            cluster.requested_no_of_instance = form.cleaned_data['noOfNodes']        
            cluster.creation_date=datetime.now()
            cluster.last_update_date=datetime.now()        
            cluster.save()           
            node = Node.objects.filter(user_id=cluster).exclude(status = Cluster.STATUS_DELETED)#change to cluster once model is created
            return render(request, 'ccloud/modifyclusterPage.html', {'form': form,'addflg' : addflg,'cid':cid,'modorview':modorview,'message':message,'node': node})
    return render(request, 'ccloud/modifyclusterPage.html', {'form': form,'addflg' : addflg,'cid':cid,'modorview':modorview,'message':message})
