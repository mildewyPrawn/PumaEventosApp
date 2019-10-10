from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

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

def Login(request):
    """
        Login to Web Page.
    """
    print(request.method)
    template = 'User/registration/login.html'
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
