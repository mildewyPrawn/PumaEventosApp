from .forms import EventosForm, StaffForm, InvitacionesForm, EtiquetaForm
from .models import Evento, Staff, Invitacion, Etiqueta
from .utils import send_email, invitacion_activacion_token, make_qr
from PIL import Image
from User.models import User, Usuario
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, ListView
import qrcode

def nuevaInvitacion(request):
    """
    Generar nueva invitación
    """
    form = InvitacionesForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect('Invitaciones')
    return render(request,'invitacionesForm.html',{'form':form})

def Invitaciones(request,evento_id):
    """
    Vista de las invitaciones
    """
    evento = Evento.objects.all()
    invitaciones= Invitacion.objects.all()
    return render(request,'invitaciones.html',{'invitaciones':invitaciones})

def RegisterEvent(request, id1, id2):
    """
    Vista para registrar un evento
    """
    evento = Evento.objects.get(pk=id1)
    # usuario = User.objects.get(pk=id2)
    usuario = request.user
    template = 'registerEvent.html'
    context = {'evento':evento, 'user':usuario}
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
        img = make_qr(message)
        img.save('images/' + str(id1) + str(request.user) + '.png')
        nombre = 'images/' + str(id1) + str(request.user) + '.png'
        im = Image.open(nombre)
        Invitacion.objects.filter(pk=id1).update(qr=im)
        content += message
        # Generar el correo en html
        email = EmailMessage(subject, content, settings.EMAIL_HOST_USER, guest)
        email.attach_file('images/' + str(id1) + str(request.user) + '.png')
        email.send()
        print(usuario.email)
        print(evento.nombre)
        return HttpResponse('Se ha enviado la invitación por correo :3')    
    return render(request, template, context)                

##########################################################################
#Events Stuff
##########################################################################

def listMyEvents(request):
    """
    Vista de listar eventos 
    """
    eventos=Evento.objects.all()
    return render(request,'myEvents.html',{'eventos':eventos})

def seeEvent(request,id):
    """
    Vista para ver un evento en específico
    """
    evento = Evento.objects.get(id=id)
    return render(request,'verEvento.html',{'evento':evento})

def createEvent(request):
    """
    Vista para crear un evento
    """
    form = EventosForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listMyEvents')
    return render(request,'eventsForm.html',{'form':form})

def updateEvent(request, id):
    """
    Vista para actualizar un evento
    """
    evento = Evento.objects.get(id=id)
    form = EventosForm(request.POST or None, instance=evento)
    if form.is_valid():
        form.save()
        return redirect('listMyEvents')
    return render(request,'eventsForm.html',{'form':form, 'evento':evento})
# EventosForm no sirve (?)

def deleteEvent(request, id):
    """
    Vista para borrar un evento
    """
    evento = Evento.objects.get(id=id)
    if request.method == 'POST':
        evento.delete()
        return redirect('listMyEvents')
    return render(request, 'prod_delete-confirm.html',{'evento':evento})

class SearchEventsView(ListView):
    """
    Vista para buscar eventos
    """
    model = Evento
    template_name = 'search_results.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Evento.objects.filter(
            # Lista de cosas por las que se puede buscar un evento
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
    """
    Agregar un staff
    """
    form = StaffForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listStaffs')
    return render(request,'staffForm.html',{'form':form})

def deleteStaff(request, id):
    """
    Borrar un staff
    """
    staff = Staff.objects.get(id=id)
    if request.method == 'POST':
        staff.delete()
        return redirect('listMyEvents')
    return render(request, 'prod_delete-confirm.html',{'staff':staff})

def listStaffs(request):
    """
    Listar a todos los staffs
    """
    eventos=Evento.objects.all()
    staffs=Staff.objects.all()
    return render(request,'myStaffs.html',{'eventos':eventos, 'staffs':staffs})

##########################################################################
# CREATE TAG
##########################################################################

def newTag(request):
    """
    Agregar un TAG
    """
    tags=Etiqueta.objects.all()
    form = EtiquetaForm(request.POST or None)
    if form.is_valid():
        form.save()
        print('ulmo')
        return redirect('createEvent')
    print('ulmo2')
    return render(request,'createTag.html',{'etiquetas':tags})
