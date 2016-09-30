from django import forms
from django.contrib.auth.models import User

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
class AddPage(forms.Form):
    giturl = forms.CharField(label='githuburl', max_length=500)
    
class ModifyPage(forms.Form):
    giturl = forms.CharField(label='githuburl', max_length=500)  