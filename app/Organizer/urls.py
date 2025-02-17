"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.urls import path
from django.urls import include, path
from .views import *

urlpatterns = [
    path('eventos/misEventos', listMyEvents,name='listMyEvents'),
    path('eventos/new', createEvent, name='createEvent'),
    path('eventos/update/<int:id>/',updateEvent,name='updateEvent'),
    path('eventos/see/<int:id>/',seeEvent,name='seeEvent'),
    path('eventos/delete/<int:id>/',deleteEvent,name='deleteEvent'),

    path('eventos/Invitacion/new', nuevaInvitacion, name='nuevaInvitacion'),
    path('eventos/Invitacion/<int:evento_id>/all', Invitaciones, name='Invitaciones'),

    ######## STAFF ########
    path('MisStaffs/new', addStaff, name='addStaff'),
    path('MisStaffs/listStaffs', listStaffs, name='listStaffs'),
    path('MisStaffs/delete/<int:id>/',deleteStaff,name='deleteStaff'),

    ######## EVENTS SEARCH ########
    path('search/', SearchEventsView.as_view(), name='search_results'),

    ######## REGISTER EVENT ########
    path('eventos/register/<str:id1>/<str:id2>', RegisterEvent, name='registerEvent'),
    # url(r'^register/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
]
