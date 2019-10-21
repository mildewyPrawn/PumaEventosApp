from django.urls import path
from django.urls import include, path
from django.contrib import admin
from . import views

app_name = 'User'
urlpatterns = [
    # Funtion view
    # path('', views.index, name='index'),
    # Class-based Views
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    #TODAS LAS SIGUIENTES DIRECCIONES VIENEN CON LA DE ARRIBA
    #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    #accounts/login/ [name='login']
    #accounts/logout/ [name='logout']
    #accounts/password_change/ [name='password_change']
    #accounts/password_change/done/ [name='password_change_done']
    #accounts/password_reset/ [name='password_reset']
    #accounts/password_reset/done/ [name='password_reset_done']
    #accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #accounts/reset/done/ [name='password_reset_complete']
    #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    path('', views.Index, name='index'),
    path('home/', views.Index, name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('login/', views.SignInView.as_view(), name='login'),
    # path('login/register.html/', views.Register, name='register'), # no sé si sirva
    path('register/', views.Register, name='register'),
    path('events/', views.Events, name='events'),
    path('events/index.html/', views.Events, name='events'),
    path('events/index/', views.Events, name='events'),
    path('events/home.html', views.Events, name='eventsHome'),
    path('events/home', views.Events, name='eventsHome'),
    path("logout", views.logout_request, name="logout"),

    path("error505", views.error505, name="error505"),


    #path('login/', views.SignInView.as_view(), name='login'),
    #path('home/login/', views.SignInView.as_view(), name='login'),
    #path('login/register.html/', views.Register, name='register'),
    #path('register/', views.Register, name='register2'),
    # path('about/', views.About.as_view(), name='about'),
    # path('login/', views.Login.as_view(), name='login'),
    # path('logout/', views.Logout.as_view(), name='logout'),
]
