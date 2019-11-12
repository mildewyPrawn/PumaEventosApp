from django.urls import path
from django.urls import include, path
from . import views
from django.conf.urls import url, include

app_name = 'User'
urlpatterns = [
    # Funtion view
    # path('', views.index, name='index'),
    # Class-based Views
    path('', views.Index, name='index'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('login/register.html/', views.Register, name='register'),
    #path('register/', views.Register, name='register2'),
    path('register/', views.SingUpView.as_view(), name='register2'),
    path('home/', views.HomeView.as_view(),name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('register/Organizador', views.RegistroOrganizador.as_view(), name='registroOrg')
    #url(r'abhsda', views.)
    # path('about/', views.About.as_view(), name='about'),
    # path('login/', views.Login.as_view(), name='login'),
    # path('logout/', views.Logout.as_view(), name='logout'),
]
