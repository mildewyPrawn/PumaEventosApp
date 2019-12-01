from .forms import CreaOrganizador, SingInForm, CreateUrs, FCambioContrasena
from .models import Usuario
from .tokens import account_activation_token
from .utils import IsNotAuthenticatedMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
import urllib

from Organizer.models import *

from .models import User
from .forms import CreateUrs, SingInForm

# from Post.models import Post
# from Home.forms import LoginForm
# Function Views


def Index(request):
    """
        Index in my Web Page.
    """
    print(request.method)
    template = 'User/general/index.html'
    context = {}
    return render(request, template, context)

def error505(request):
    print(request.method)
    template = 'User/general/505.html'
    context = {}
    return render(request, template, context)

class HomeView(LoginRequiredMixin, CreateView):
    template = 'User/indexpl.html'
    def get(self, request):
        return render(request, self.template)

#Login que si hace algo.
class SignUpView(View):
    #model = Usuario
    template = 'User/registration/register.html'
    context = {}

    def get(self, request):
        form = CreateUrs()
        #form2 = SingUpForm()
        return render(request, self.template)

    def post(self, request):
        form = CreateUrs(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            
            #user2 = Usuario.create_user_Usuario(user, form.clean_avatar)
            user.is_active = False
            user.save()
            user2 = Usuario(
                user=user, 
                avatar=form.clean_avatar(),
                es_Organizador = False,
                es_Staff = False
            )
            user2.save()
            #print(user)
            current_site = get_current_site(request)
            """
            if condicion:
                form.add.errors(field, error)
            """
            mail_subject = 'Activate your PumaEventos account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            #context = {"message":'Please confirm your email address to complete the registration'}
            context ={"msg":"1"}
            return redirect('/../home/?' + urllib.parse.urlencode(context))
            #return HttpResponse('Please confirm your email address to complete the registration')
        else:
            self.context['form'] = form
        #print(form.errors, "asdads")
        return render(request, self.template, self.context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        # messages.info(request,'Thank you for your email confirmation. Now you can login your account.')
        #return HttpResponseRedirect('/login/')
        #context={"message":'Thank you for your email confirmation. Now you can login your account.'}
        context ={"msg":"2"}
        return redirect('/../home/?' + urllib.parse.urlencode(context) )
    else:
        #return HttpResponse('Activation link is invalid!')
        context ={"msg":"3"}
        return redirect('/../home/?' + urllib.parse.urlencode(context) )

def activateEvent(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            inv = Invitacion.objects.get(pk=uid)
            print('>>>>>>')
            print(inv)
            print('>>>>>>')
        except(TypeError, ValueError, OverflowError):
            inv = None
        if inv is not None:
            Invitacion.objects.filter(pk=uid).update(activa=False,
                                                     asistencia_activa=True)
            print('+++', inv.asistencia_activa)
            if inv.asistencia_activa:
                return HttpResponse('Su presencia ya fue registrada.')                
            return HttpResponse('Su presencia ha sido registrada.')
        else:
            return HttpResponse('Su presencia ya fue registrada.')

class RegistroOrganizador(LoginRequiredMixin, View):
    template = "User/registration/registrOrgnz.html"
    context = {}
    
    def get(self, request):
        if request.user.is_superuser:
            form = CreaOrganizador()
            return render(request, self.template, self.context)
        return redirect('/eventos/')

    def post(self, request):
        form = CreaOrganizador(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user2 = Usuario(
                user=user,
                avatar = form.clean_avatar(),
                es_Organizador = True,
                es_Staff = False,
            )
            user2.save()
            current_site = get_current_site(request)
            """
            if condicion:
                form.add.errors(field, error)
            """
            mail_subject = 'Activate your PumaEventos account.'
            message = render_to_string('acc_active_org.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            #Add render page, Usuario creado
            return HttpResponse("Creado weon")
        else:
            self.context['form'] = form
        return render(request, self.template, self.context)  

def activateO(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        #redirect()
        return redirect('/register/cambioContrasena')
    else:
        return HttpResponse('Activation link is invalid!')

class CambioContrasena(View):
    template = "User/registration/cambioContra.html"
    context = {}

    def get(self, request):
        form = FCambioContrasena(request.user)
        return render(request, self.template, self.context)

    def post(self, request):
        form = FCambioContrasena(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            logout(request)
            return redirect('register/login/')
        else:
            self.context['form'] = form
        return render(request, self.template, self.context)

#Login que si hace algo.
class SignInView(IsNotAuthenticatedMixin ,View):
    #template_name = 'User/registration/login.html'
    template = 'User/registration/login.html'
    context = {}

    def get(self, request):
        form = SingInForm()
        #print("im here")
        return render(request, self.template)
    
    def post(self, request):
        """
            Validates and do the login
        """
        #if request.user.is_authenticated():
        #    return redirect('/home/')
        form = SingInForm(request.POST)
        #print("im here") 
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            #print(user, "asdasdasdad")
            if user is not None:
                login(request, user)
                if request.GET.get("next", None) is not None:
                    return redirect(request.GET.get("next"))
                return redirect('/eventos/')
            #messages.add_message(request, messages.INF ─O, 'Hello world.')
            form.add_error("username","Usuario o contraseña erroneos.")
            self.context['form'] = form
            #print(form.errors)
            return render(request, self.template, self.context)
        return render(request, self.template, self.context)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("/")

def Register(request):
    """
        Register to app.
    """
    print(request.method)
    template = 'User/registration/register.html'
    context = {}
    return render(request, template, context)

class EventosN(LoginRequiredMixin, CreateView):
    context = {}
    template = 'User/eventos/home.html'

    def get(self, request):
        print(request.method)
        user = request.user
        print("...............................")
        print(user)
        #print()
        print("...............................")
        self.context = {'user':user}
        return render(request, self.template, self.context)

def Eventos(request):
    """
        Eventos home Page
    """
    print(request.method)
    template = 'User/eventos/home.html'
    user = request.user
    print("...............................")
    print(user)
    # print(request.user.usuario.avatar.url)
    print("...............................")
    context = {'user':user}
    return render(request, template, context)



def EventosList(request):
    """
        All Eventos home Page
    """
    print(request.method)
    template = 'User/eventos/all.html'
    user = request.user.get_username()
    eventos = Evento.objects.all()

    print("...............................")
    print(user)
    print("...............................")
    context = {'user':user,'eventos':eventos}
    return render(request, template, context)

def logout_request(request):
    template = 'User/general/index.html'
    context ={}
    logout(request)
    return render(request,template,context)

class About(View):
    """
        About me page.
    """
    template = 'User/general/about.html'
    context = {'title': 'About me'}

    def get(self, request):
        """
            Get in About me.
        """
        return render(request, self.template, self.context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
