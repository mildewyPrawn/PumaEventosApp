from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from .utils import IsNotAuthenticatedMixin
from django.contrib import messages
from .models import Usuario
from django.http import HttpResponseRedirect
from .forms import SingUpForm, SingInForm, CreateUrs
# from Post.models import Post
# from Home.forms import LoginForm
# Function Views

def Index(request):
    """
        Index in my Web Page.
    """
    print(request.method)
    template = 'User/index.html'
    context = {}
    return render(request, template, context)

class HomeView(LoginRequiredMixin, CreateView):
    template = 'User/indexpl.html'
    def get(self, request):
        return render(request, self.template)

class SingUpView(CreateView):
    #model = Usuario
    template = 'User/registration/register.html'
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
            user2 = Usuario(user=user, avatar=form.clean_avatar())
            user2.save()
            print(user)
            #messages.info(request, 'Your password has been changed successfully!')
            #return HttpResponseRedirect("/")
            #return redirect('/home/')
        print(form.errors)
        return render(request, self.template)


    #def form_valid(self, form):   
    #    return redirect('/')

#Login que si hace algo.
class SignInView( View):
    #template_name = 'User/registration/login.html'
    template = 'User/registration/login.html'
    def get(self, request):
        form = SingInForm()
        
        return render(request, self.template)

    def post(self, request):
        """
            Validates and do the login
        """
        #if request.user.is_authenticated():
        #    return redirect('/home/')
        form = SingInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get("next", None) is not None:
                    return redirect(request.GET.get("next"))
                return redirect('/home/')
            #messages.add_message(request, messages.INFO, 'Hello world.')
            return render(request, self.template)
        #self.context['form'] = form
        return render(request, self.template)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("/")

def Register(request):
    """
        Login to Web Page.
    """
    print(request.method)
    template = 'User/registration/register.html'
    context = {}
    return render(request, template, context)

class About(View):
    """
        About me page.
    """
    template = 'Home/about.html'
    context = {'title': 'About me'}

    def get(self, request):
        """
            Get in About me.
        """
        return render(request, self.template, self.context)
