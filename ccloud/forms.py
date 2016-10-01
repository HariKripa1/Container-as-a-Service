from django import forms
from django.contrib.auth.models import User
from .models import Container

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
class AddPage(forms.Form):
    containername = forms.CharField(label='Container Name', max_length=500)
    giturl = forms.CharField(label='GIT Hub URL', max_length=500)
    dockerfilereq = forms.BooleanField(label='Docker file required', initial=False, required=False)
    application = forms.ChoiceField(choices=Container.APPLICATION_CHOICES)
    
class ModifyPage(forms.Form):    
    containername = forms.CharField(label='Container Name', max_length=500)
    giturl = forms.CharField(label='GIT Hub URL', max_length=500)
    dockerfilereq = forms.BooleanField(label='Docker file required', initial=False, required=False)
    application = forms.ChoiceField(choices=Container.APPLICATION_CHOICES)