from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Usuario

class SingInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password')

class SingUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=42)
    apellido = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
