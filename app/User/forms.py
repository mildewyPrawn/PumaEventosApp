from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import User

class SingInForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña')

class SingUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(max_length=254,
                             help_text='Requerido, necesitas una dirección de email váilda.')
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    user = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'email',
                  'user',
                  'avatar',
                  'password'] 
