from .models import Evento,Staff,Invitacion, Etiqueta
from django import forms

class EventosForm(forms.ModelForm):
    """
    Datos que pedimos para registrar un evento
    """
    class Meta:
	    model= Evento
	    fields= ['nombre','descripcion','fecha_inicio', 'fecha_fin', 
		     'direccion', 'horario_inicio', 'horario_fin', 'capacidad', 
		     'etiqueta','organizador']
		
class StaffForm(forms.ModelForm):
    """
    Datos para el staff.
    """
    class Meta:
	    model = Staff
	    fields = ['user_id','evento_id']

class InvitacionesForm(forms.ModelForm):
    """
    Datos que se piden para mandar una invitación.
    """
    class Meta(object):
	    model = Invitacion
	    fields = ['evento_id','user_id','activa','asistencia_activa', 'qr',]

class EtiquetaForm(forms.ModelForm):
    """
    Datos para la etiqueta
    """
    class Meta:
	    model = Etiqueta
	    fields = ['nombre']
