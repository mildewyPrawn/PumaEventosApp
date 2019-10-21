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
    template = 'User/general/index.html'
    context = {}
    return render(request, template, context)














def Register(request):
    """
        Login to Web Page.
    """
    print(request.method)
    template = 'User/registration/register.html'
    context = {}
    return render(request, template, context)


def Events(request):
    """
        Events home Page
    """
    print(request.method)
    template = 'User/events/home.html'
    user = request.user.get_username()
    print("...............................")
    print(user)
    print("...............................")
    context = {'user':user}
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
