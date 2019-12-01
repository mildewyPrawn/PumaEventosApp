from django import forms
from .models import Evento,Staff,Invitacion



class EventosForm(forms.ModelForm):
	class Meta:
		model= Evento
		fields= ['nombre','descripcion','fecha_inicio', 'fecha_fin', 
				'direccion', 'horario_inicio', 'horario_fin', 'capacidad', 
				'etiqueta','organizador']
		

class StaffForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields = ['user_id','evento_id']


class InvitacionesForm(forms.ModelForm):
	class Meta(object):
		model = Invitacion
		fields = ['evento_id','user_id','activa','asistencia_activa', 'qr',]
