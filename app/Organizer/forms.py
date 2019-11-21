from django import forms
from .models import Evento,Staff



class EventosForm(forms.ModelForm):
	class Meta:
		model= Evento
		fields=['nombre','descripcion','fecha_inicio', 'fecha_fin', 
				'direccion', 'horario_inicio', 'horario_fin', 'capacidad', 
				'etiqueta','organizador']
		

class StaffForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields =['user_id','evento_id']		