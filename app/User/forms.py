from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.core.files.images import get_image_dimensions


from .models import Usuario

class SingInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password')

class CreateUrs(UserCreationForm):
    class Meta:
        avatar = forms.ImageField(required=False)
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            #'avatar',
        )

class SingUpForm(UserCreationForm):
    #email = forms.EmailField(max_length=200, help_text='Required', required=True)

    avatar = forms.ImageField(required=False)
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        #password = forms.CharField(widget=forms.PasswordInput)
        model = Usuario
        fields = (
            #'user__username',
            'avatar',
            'email',
        )
    
    #def save(self, commit=True):
    #    user = super(SingUpForm, self).save(commit=False)

    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('unam.mx'):
            raise ValidationError('El dominio no es valido.')
        return email
    
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            w, h = get_image_dimensions(avatar)
            if w > 500 or h > 500:
                raise ValidationError(u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (100, 100))
        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar

