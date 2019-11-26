from django.shortcuts import render,redirect,render_to_response
from .models import Evento
from .forms import EventosForm
from django.views.generic import View
from django.db.models import Q
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

#Busca los eventos.
def buscarEventos(request):
	query = request.GET.get('q','')
	if query:
		qset = (
			Q(nombre = query) |
			Q(descripcion = query) |
			Q(etiqueta = query)
		)
		resultado = Evento.objects.filter(qset).distinct()
	else:
		resultado = []
		return render_to_response("buscarEventos.html",{
			"resultado": resultado,
			"query": query,
			})
	return render(request,'buscarEventos.html',{'evento':evento})

class ResultadoView(View):
    form_class = EventosForm
    template_name = "buscarEventos.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()