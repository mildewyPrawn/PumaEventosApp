from .forms import EventosForm, StaffForm, InvitacionesForm
from .models import Evento, Staff, Invitacion
from .utils import send_email, invitacion_activacion_token, make_qr
from PIL import Image
from User.models import User, Usuario
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, ListView
import qrcode

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

# def RegisterEvent(request, id, user):
def RegisterEvent(request, id1, id2):
        evento = Evento.objects.get(pk=id1)
        usuario = User.objects.get(pk=id2)
        template = 'registerEvent.html'
        context = {'evento':evento, 'user':usuario}
        # context = {}
        if request.method == 'POST':
                current_site = get_current_site(request)
                subject = 'Invitación a ' + evento.nombre
                content = 'Tienes una cita el día: ' + str(evento.fecha_inicio) + ' para el evento: ' + evento.nombre
                guest = [usuario.email]
                inv_count = Invitacion.objects.filter(evento_id=id1).count()
                print('COUNT>>', inv_count)
                inv = Invitacion(evento_id=evento, user_id=usuario, activa=True,
                                 asistencia_activa=False)
                inv.save()
                if inv_count > evento.capacidad:
                        return HttpResponse('Ya no hay lugares disponibles :(')
                message = render_to_string('registration_mail.html', {
                        'user': usuario,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(inv.pk)),
                        'token':invitacion_activacion_token.make_token(inv), # esto me causa dudas
                })
                # content += message
                img = make_qr(message)
                img.save('images/' + id1 + id2 + '.png')
                nombre = 'images/' + id1 + id2 + '.png'
                im = Image.open(nombre)
                Invitacion.objects.filter(pk=id1).update(qr=im)

                content += message
                msge = EmailMultiAlternatives(subject=subject, body=content, from_email=settings.EMAIL_HOST_USER, to=guest)
                # html_template = get_template('mail.html').render()
                html_template = '<h1>Hola '+usuario.username+'</h1>\n'
                html_template += '<h2>Por favor enseña el siguiente código a un miembro del staff para registrar tu entrada:</h2>'
                html_template += '<img src=images/12.png.url enctype="multipart/form-data">'
                html_template += message
                # html_tempalte += '<img src=' + 12.png.url + '>'
                msge.attach_alternative(html_template, 'text/html')
                msge.send()
                # send_email(guest, subject, content)
                # print (user)
                # print(id1)
                print(usuario.email)
                print(evento.nombre)
                return HttpResponse('Se ha enviado la invitación por correo :3')
                
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


