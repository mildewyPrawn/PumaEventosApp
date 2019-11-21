from django.shortcuts import render,redirect
from .models import Evento, Staff
from .forms import EventosForm, StaffForm

# Create your views here.


def listMyEvents(request):
	eventos=Evento.objects.all()
	return render(request,'myEvents.html',{'eventos':eventos})

def seeEvent(request,id):
	evento = Evento.objects.get(id=id)
	return render(request,'verEvento.html',{'evento':evento})


def createEvent(request):
	form = EventosForm(request.POST or None)

	if form.is_valid():
		form.save()
		return redirect('listMyEvents')

	return render(request,'eventsForm.html',{'form':form})


def updateEvent(request, id):
	evento = Evento.objects.get(id=id)
	form = EventosForm(request.POST or None, instance=evento)

	if form.is_valid():
		form.save()
		return redirect('listMyEvents')

	return render(request,'eventsForm.html',{'form':form, 'evento':evento})


def deleteEvent(request, id):
	evento = Evento.objects.get(id=id)
	if request.method == 'POST':
		evento.delete()
		return redirect('listMyEvents')

	return render(request, 'prod_delete-confirm.html',{'evento':evento})


def addStaff(request):
	form = StaffForm(request.POST or None)

	if form.is_valid():
		form.save()
		return redirect('listStaffs')

	return render(request,'staffForm.html',{'form':form})

def deleteStaff(request, id):
	staff = Staff.objects.get(id=id)
	if request.method == 'POST':
		staff.delete()
		return redirect('listMyEvents')

	return render(request, 'prod_delete-confirm.html',{'staff':staff})


def listStaffs(request):
	eventos=Evento.objects.all()
	staffs=Staff.objects.all()
	return render(request,'myStaffs.html',{'eventos':eventos, 'staffs':staffs})


