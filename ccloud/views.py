# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django import forms
from .forms import NameForm, UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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
            return HttpResponseRedirect('/thanks/')

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
    			return HttpResponseRedirect('/ccloud/')
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
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/ccloud/')


