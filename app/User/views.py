from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView

from .models import Usuario
from .forms import SingUpForm, SingInForm
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

class SingUpView(CreateView):
    model = Usuario
    form = SingUpForm
    def form_valid(self, form):
        #Envio de correo aun no implementado
        return redirect('/')

#Login que si hace algo.
class SignInView(LoginView):
    #template_name = 'User/registration/login.html'
    template = 'User/registration/login.html'
    def get(self, request):
        form = SingInForm()
        return render(request, self.template)

    def post(self, request):
        """
            Validates and do the login
        """
        form = SingInForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get("next", None) is not None:
                    return redirect(request.GET.get("next"))
                return redirect('/')

        #self.context['form'] = form
        return render(request, self.template)



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
