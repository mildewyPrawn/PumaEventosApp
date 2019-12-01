from django import forms
import random
import string
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.forms import ValidationError
from .models import Usuario

class SingInForm(forms.Form):
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña')

class CreateUrs(UserCreationForm):
    avatar = forms.ImageField(required=False, help_text='Puedes no poner una imagen.')
    #def __init__(self, *args, **kwargs):
    #    super(CreateUrs, self).__init__(*args, **kwargs)
    #    for field_name, field in self.fields.items():
    #        field.required = True

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            #'avatar',
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('unam.mx'):
            raise ValidationError('El dominio no es valido.')
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        print(avatar)
        if avatar is None:
            return None
        #retunr null
        try:
            w, h = get_image_dimensions(avatar)
            #if w > 1000 or h > 1000:
            #    raise ValidationError(u'Please use an image that is '
            #         '%s x %s pixels or smaller.' % (100, 100))
            return avatar
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar
    
    def save(self, commit=True):
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password2')
        #avatar = self.clean_avatar()
        user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name,
                                        email=email, password=password)
        #user.is_active = False
        #user1 = Usuario.create_user_Usuario(user, avatar)
        #user.set_username()
        #user1 = user.get
        if commit:
            #user.save()
            #return user
            pass
        return user

class FCambioContrasena(ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(FCambioContrasena, self).__init__(*args, **kwargs)
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password2'])
        if commit:
            self.user.save()
        return self.user

    class Meta:
        model = User
        fields = (
            'password1',
            'password2',
        )

class CreaOrganizador(ModelForm):
    #email = forms.EmailField(max_length=200, help_text='Required', required=True)
    #avatar = forms.ImageField(required=False)
    #email = forms.EmailField(max_length=200, help_text='Required'perla)
    avatar = forms.ImageField(required=False, help_text='Puedes no poner una imagen.')

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('unam.mx'):
            raise ValidationError('El dominio no es valido.')
        return email
    
    def randPasw(self):
        letters = string.ascii_lowercase
        return ''.join(random.sample(letters, 9))

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        print(avatar)
        if avatar is None:
            return None
        #retunr null
        try:
            w, h = get_image_dimensions(avatar)
            #if w > 1000 or h > 1000:
            #    raise ValidationError(u'Please use an image that is '
            #         '%s x %s pixels or smaller.' % (100, 100))
            return avatar
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar
    
    def save(self, commit=True):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.randPasw()
        user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, email=email, password=password)
        if commit:
            pass
        return user