from django.urls import path
from django.urls import include, path
from . import views

app_name = 'User'
urlpatterns = [
    # Funtion view
    # path('', views.index, name='index'),
    # Class-based Views
    path('', views.Index, name='index'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('login/register.html/', views.Register, name='register'),
    path('register/', views.Register, name='register2'),
    path('events/', views.Events, name='events'),
    path('events/index.html/', views.Events, name='events'),
    path('events/index/', views.Events, name='events'),
    path('events/home.html', views.Events, name='eventsHome'),
    path('events/home', views.Events, name='eventsHome'),

    # path('about/', views.About.as_view(), name='about'),
    # path('login/', views.Login.as_view(), name='login'),
    # path('logout/', views.Logout.as_view(), name='logout'),
]
