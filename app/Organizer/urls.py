from .views import *
from django.conf import settings
from django.conf.urls import url, include
from django.urls import include, path
from django.urls import path

"""
Urls de Organizer
"""
urlpatterns = [
    path('eventos/Invitacion/<int:evento_id>/all', Invitaciones,
         name='Invitaciones'),
    path('eventos/Invitacion/new', nuevaInvitacion, name='nuevaInvitacion'),
    path('eventos/delete/<int:id>/',deleteEvent,name='deleteEvent'),
    path('eventos/misEventos', listMyEvents,name='listMyEvents'),
    path('eventos/new', createEvent, name='createEvent'),
    path('eventos/see/<int:id>/',seeEvent,name='seeEvent'),
    path('eventos/update/<int:id>/',updateEvent,name='updateEvent'),
    ######## STAFF ########
    path('MisStaffs/delete/<int:id>/',deleteStaff,name='deleteStaff'),
    path('MisStaffs/listStaffs', listStaffs, name='listStaffs'),
    path('MisStaffs/new', addStaff, name='addStaff'),
    ######## EVENTS SEARCH ########
    path('search/', SearchEventsView.as_view(), name='search_results'),
    ######## REGISTER EVENT ########
    path('eventos/register/<str:id1>/<str:id2>', RegisterEvent,
         name='registerEvent'),
    ######## CREATE TAG ########
    path('tags', newTag, name='newTag'),
]
