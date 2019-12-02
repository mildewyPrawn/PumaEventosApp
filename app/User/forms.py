from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.forms import ModelForm
from django.forms import ValidationError
import random
import string

class SingInForm(forms.Form):
    """
    Iniciar sesión
    """
    username = forms.CharField(label='Usuario', max_length=100)
    password = forms.CharField(label='Contraseña')

class CreateUrs(UserCreationForm):
    """
    Crear usuarios
    """
    avatar = forms.ImageField(required=False,
                              help_text='Puedes no poner una imagen.')
    entidad = forms.CharField(required=True)

    class Meta:
        """
        Datos que se piden al nuevo usuario
        """
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def clean_email(self):
        """
        Validar email
        """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ese correo ya fue registrado.')
        if not email.endswith('unam.mx'):
            raise ValidationError('El dominio no es valido.')
        return email
    
    def clean_entidad(self):
        entidad = self.cleaned_data['entidad']
        return entidad

    def clean_avatar(self):
        """
        Verificar el avatar
        """
        avatar = self.cleaned_data['avatar']
        print(avatar)
        if avatar is None:
            return None
        try:
            w, h = get_image_dimensions(avatar)
            return avatar
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar
    
    def save(self, commit=True):
        """
        Crea un nuevo usuario y lo regresa
        """
        username = self.cleaned_data.get('username')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password2')
        user = User.objects.create_user(username=email, first_name=first_name,
                                        last_name=last_name, email=email,
                                        password=password)
        if commit:
            pass
        return user

class FCambioContrasena(ModelForm):
    """
    Formulario para cambiar contraseña, esto solo se usa en organizador
    """
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(FCambioContrasena, self).__init__(*args, **kwargs)
    
    def clean_password1(self):
        """
        Verificar contraseñas
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        """
        Guardar nueva contraseña
        """
        self.user.set_password(self.cleaned_data['password2'])
        if commit:
            self.user.save()
        return self.user

    class Meta:
        """
        Datos que pedimos para cambiar la contraseña
        """
        model = User
        fields = (
            'password1',
            'password2',
        )

class CreaOrganizador(ModelForm):
    """
    Crear un organizador, solo el admin puede hacerlo
    """
    avatar = forms.ImageField(required=False,
                              help_text='Puedes no poner una imagen.')

    class Meta:
        """
        Datos que se piden para ser organizador.
        """
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
    
    def clean_email(self):
        """
        Verificación del email
        """
        email = self.cleaned_data['email']
        if not email.endswith('unam.mx'):
            raise ValidationError('El dominio no es valido.')
        return email
    
    def randPasw(self):
        """
        Genera una contraseña al azar para después cambiarla
        """
        letters = string.ascii_lowercase
        return ''.join(random.sample(letters, 9))

    def clean_avatar(self):
        """
        Verifica el avatar
        """
        avatar = self.cleaned_data['avatar']
        print(avatar)
        if avatar is None:
            return None
        try:
            w, h = get_image_dimensions(avatar)
            return avatar
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar
    
    def save(self, commit=True):
        """
        Guarda un nuevo administrador
        """
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        password = self.randPasw()
        user = User.objects.create_user(username=email, first_name=first_name,
                                        last_name=last_name, email=email,
                                        password=password)
        if commit:
            pass
        return user
