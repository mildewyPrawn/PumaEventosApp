from .forms import EventosForm, StaffForm, InvitacionesForm
from .models import Evento, Staff, Invitacion
from django.db.models import Q
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView

# Create your views here.


def nuevaInvitacion(request):
	form = InvitacionesForm(request.POST or None)

	if form.is_valid():
		form.save()
		return redirect('Invitaciones')

	return render(request,'invitacionesForm.html',{'form':form})

def Invitaciones(request,evento_id):
	evento = Evento.objects.all()
	invitaciones= Invitacion.objects.all()
	return render(request,'invitaciones.html',{'invitaciones':invitaciones})

def RegisterEvent(request):
    template = 'registerEvent.html'
    context = {}
    return render(request, template, context)


##########################################################################
#Events Stuff
##########################################################################


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
EventosForm

def deleteEvent(request, id):
	evento = Evento.objects.get(id=id)
	if request.method == 'POST':
		evento.delete()
		return redirect('listMyEvents')

	return render(request, 'prod_delete-confirm.html',{'evento':evento})



class SearchEventsView(ListView):
        model = Evento
        template_name = 'search_results.html'

        def get_queryset(self): # new
                query = self.request.GET.get('q')
                object_list = Evento.objects.filter(
                        Q(nombre__icontains=query) |
                        Q(descripcion__icontains=query) |
                        Q(direccion__icontains=query) |
                        Q(fecha_inicio__icontains=query) | 
                        Q(etiqueta__nombre__icontains=query)
                )
                return object_list


##########################################################################
#Staff Stuff
##########################################################################

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


