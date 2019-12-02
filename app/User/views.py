from .forms import CreaOrganizador, SingInForm, CreateUrs, FCambioContrasena
from .forms import CreateUrs, SingInForm
from .models import User
from .models import Usuario
from .tokens import account_activation_token
from .utils import IsNotAuthenticatedMixin
from Organizer.models import *
from django.contrib import messages
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
import urllib

def Index(request):
    """
    Index de la página web
    """
    print(request.method)
    template = 'User/general/index.html'
    context = {}
    return render(request, template, context)

def error505(request):
    """
    Sino encuentra una url, muestra un lindo mensaje.
    """
    print(request.method)
    template = 'User/general/505.html'
    context = {}
    return render(request, template, context)

class HomeView(CreateView):
    """
    Vista principal
    """
    template = 'User/general/index.html'
    def get(self, request):
        return render(request, self.template)

class SignUpView(View):
    """
    Vista para registrarse
    """
    template = 'User/registration/register.html'
    context = {}

    def get(self, request):
        form = CreateUrs()
        return render(request, self.template)

    def post(self, request):
        """
        Te registra y manda correo de verificación
        """
        form = CreateUrs(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user2 = Usuario(
                user=user, 
                avatar=form.clean_avatar(),
                es_Organizador = False,
                es_Staff = False,
                entidad = form.clean_entidad(),
            )
            user2.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your PumaEventos account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            # Mandar correo
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            context ={"msg":"1"}
            # Avisa de que el correo ha sido enviado
            return redirect('/../home/?' + urllib.parse.urlencode(context))
        else:
            self.context['form'] = form
        return render(request, self.template, self.context)

def activate(request, uidb64, token):
    """
    Activa la nueva cuenta, con el link que se manda por correo
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        logout(request)
        context ={"msg":"2"}
        return redirect('/../home/?' + urllib.parse.urlencode(context) )
    else:
        context ={"msg":"3"}
        return redirect('/../home/?' + urllib.parse.urlencode(context) )

def activateEvent(request, uidb64, token):
    """
    Da la activación para una invitación a un evento
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        inv = Invitacion.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        inv = None
    if inv is not None:
        Invitacion.objects.filter(pk=uid).update(activa=False,
                                                 asistencia_activa=True)
        # Si ya estaba activo no se puede registrar de nuevo
        if inv.asistencia_activa:
            return HttpResponse('Su presencia ya fue registrada.')                
        return HttpResponse('Su presencia ha sido registrada.')
    else:
        return HttpResponse('Su presencia ya fue registrada.')

class RegistroOrganizador(LoginRequiredMixin, View):
    """
    Vista para registrar a un organizador, solo el admin puede
    """
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
            mail_subject = 'Activate your PumaEventos account.'
            message = render_to_string('acc_active_org.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            # manda correo de confirmación
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse("Ha sido registrado.")
        else:
            self.context['form'] = form
        return render(request, self.template, self.context)  

def organizador_registrado(request, uidb64, token):
    """
    Verifica el registro de un organizador
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/register/cambioContrasena')
    else:
        return HttpResponse('Activation link is invalid!')

class CambioContrasena(View):
    """
    Vista para cambiar de contraseña
    """
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
            return redirect('/login/')
        else:
            self.context['form'] = form
        return render(request, self.template, self.context)

class SignInView(IsNotAuthenticatedMixin ,View):
    """
    Vista para iniciar sesión
    """
    template = 'User/registration/login.html'
    context = {}

    def get(self, request):
        form = SingInForm()
        return render(request, self.template)
    
    def post(self, request):
        """
        Valida y hace el login
        """
        form = SingInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get("next", None) is not None:
                    return redirect(request.GET.get("next"))
                return redirect('/eventos/')
            form.add_error("username","Usuario o contraseña erroneos.")
            self.context['form'] = form
            return render(request, self.template, self.context)
        return render(request, self.template, self.context)

class LogoutView(LoginRequiredMixin, View):
    """
    Hace el logout, redige a la landing page
    """
    def get(self, request):
        logout(request)
        return redirect("/")

def Register(request):
    """
    Registrarse en la aplicación
    """
    print(request.method)
    template = 'User/registration/register.html'
    context = {}
    return render(request, template, context)

class EventosN(LoginRequiredMixin, CreateView):
    """
    Vista de los eventos
    """
    context = {}
    template = 'User/eventos/home.html'

    def get(self, request):
        print(request.method)
        user = request.user
        print("...............................")
        print(user)
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
    print("...............................")
    context = {'user':user}
    return render(request, template, context)



def EventosList(request):
    """
    Todos los eventos en el home
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
    """
    Hace logout
    """
    template = 'User/general/index.html'
    context ={}
    logout(request)
    return render(request,template,context)

class About(View):
    """
    Página del about
    """
    template = 'User/general/about.html'
    context = {'title': 'About me'}

    def get(self, request):
        """
        Ingresa al about
        """
        return render(request, self.template, self.context)

def signup(request):
    """
    Hace el registro (No en uso)
    """
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
