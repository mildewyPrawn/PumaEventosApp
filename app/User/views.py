from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from Organizer.models import *

from .models import User
from .forms import SingUpForm, SingInForm
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

class SingUpView(CreateView):
    model = User
    form = SingUpForm
    def form_valid(self, form):
        #Envio de correo aun no implementado
        return redirect('/')

#Login que si hace algo.
class SignInView(View):
    template = 'User/registration/login.html'
    def get(self, request):
        form = SingInForm()
        print("im here")
        return render(request, self.template)
    
    def post(self, request):
        """
            Validates and do the login
        """
        #if request.user.is_authenticated():
        #    return redirect('/home/')
        form = SingInForm(request.POST)
        print("im here")
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user, "asdasdasdad")
            if user is not None:
                login(request, user)
                if request.GET.get("next", None) is not None:
                    return redirect(request.GET.get("next"))
                return redirect('../eventos')
            #messages.add_message(request, messages.INFO, 'Hello world.')
            return render(request, self.template)
        #self.context['form'] = form
        return render(request, self.template)

def Register(request):
    """
        Register to app.
    """
    print(request.method)
    template = 'User/registration/register.html'
    context = {}
    return render(request, template, context)

class Eventos(LoginRequiredMixin, CreateView):
    def get(self, request):
        print(request.method)
        template = 'User/eventos/home.html'
        user = request.user.get_username()
        print("...............................")
        print(user)
        print("...............................")
        context = {'user':user}
        return render(request, template, context)

def Eventos(request):
    """
        Eventos home Page
    """
    print(request.method)
    template = 'User/eventos/home.html'
    user = request.user.get_username()
    print("...............................")
    print(user)
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
