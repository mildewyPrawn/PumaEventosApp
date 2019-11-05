from django.shortcuts import render,redirect
from .models import Evento
from .forms import eventsForm

# Create your views here.


def listMyEvents(request):
	events=Evento.objects.all()
	return render(request,'myEvents.html',{'events':events})



def createEvent(request):
	form = EventoForm(request.Post or None)

	if form.is_valid():
		form.save()
		return redirect('listMyEvents')

	return render(request,'eventsForm.html',{'form':form})


def updateEvent(request):
	event = Evento.objects.get(id=id)
	form = EventoForm(request.Post or None, instance=event)

	if form.is_valid():
		form.save()
		return redirect('listMyEvents')

	return render(request,'eventsForm.html',{'form':form})


def deleteEvent(request):

	pass

