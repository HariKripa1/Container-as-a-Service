from django import forms
from django.contrib.auth.models import User
from .models import Container
from .models import Cluster

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
    port = forms.CharField(label='Port', max_length=500)    

    
class AdminAddPage(forms.Form):
    user = forms.ModelChoiceField(queryset = User.objects.all() )
    containername = forms.CharField(label='Container Name', max_length=500)
    giturl = forms.CharField(label='GIT Hub URL', max_length=500)
    port = forms.CharField(label='Port', max_length=500)        
    
class ModifyPage(forms.Form):        
    scale = forms.CharField(label='Scale', max_length=500)

class AddClusterPage(forms.Form):
    clustername = forms.CharField(label='Cluster Name', max_length=500)
    noOfNodes = forms.IntegerField(label='No of Nodes', max_value=3, min_value=1)

class ModifyClusterPage(forms.Form):
    noOfNodes = forms.IntegerField(label='No of Nodes', max_value=3, min_value=1)    

class AdminAddClusterPage(forms.Form):
    user = forms.ModelChoiceField(queryset = User.objects.all() )
    clustername = forms.CharField(label='Cluster Name', max_length=500)
    noOfNodes = forms.IntegerField(label='No of Nodes', max_value=3, min_value=1)
