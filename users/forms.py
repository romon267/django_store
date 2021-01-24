from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Shows what it is going to create
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')