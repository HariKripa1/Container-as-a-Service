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
from .models import Container
from .models import RequestQueue
from django.contrib.auth.models import User
from datetime import datetime

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

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            registered = True

        # Invalid form or forms - mistakes or something else?
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
    	if user:
    		if user.is_active:
    			login(request,user)    			
    			request.session['username'] = username
    			return HttpResponseRedirect('/ccloud/mainPage/')
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

def getMainform(request):        
    username=request.session.get('username')
    user = User.objects.get(username=username)
    container = Container.objects.filter(user_id=user).exclude(status = Container.STATUS_DELETED)
    print(request.session.get('username'))
    #return render(request, 'ccloud/mainPage.html', {'list': zip(containerId,containerNames)} )
    return render(request, 'ccloud/mainPage.html', {'container': container } )

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
            return render(request, 'ccloud/addPage.html', {'form': form,'addflg' : addflg})
    else:
        print('add page 2')
        form = AddPage()                
    return render(request, 'ccloud/addPage.html', {'form': form,'addflg' : addflg})

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
        container = Container.objects.filter(id=c_id)
        container.delete()
        modifyflg = True;
        delmodflg = 'Delete'
        return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg,'delmodflg' : delmodflg})
    else:
        if form.is_valid():
            # add in db
            form.cleaned_data['giturl']   
            c_id = request.POST.get('cid', None)
            message = "modification request sent for "+form.cleaned_data['giturl']
            context = {'message' : message, 'modifyflg' : modifyflg}    
            modifyflg = True;
            user = User.objects.get(username=username)
            container = Container.objects.filter(id=c_id)
            container.delete()
            container=Container(container_name=form.cleaned_data['containername'],git_url=form.cleaned_data['giturl'],user_id=user,docker_file=form.cleaned_data['dockerfilereq'],application_name=form.cleaned_data['application'],status=Container.STATUS_FORMODIFY,container_url='',devstack_container_id='',creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
            container.save()
            crreq=RequestQueue(container_id = container,status = RequestQueue.STATUS_FORMODIFY, creation_date=datetime.now(),last_update_date=datetime.now(),created_by=username)
            crreq.save()
            delmodflg = 'Modify'
            return render(request, 'ccloud/modifyPage.html', {'form': form,'cid':c_id,'modifyflg' : modifyflg,'delmodflg' : delmodflg})
        else:
            message = " error "
            context = {'message' : message, 'modifyflg' : modifyflg}
    return render(request, 'ccloud/thanks.html', context)

