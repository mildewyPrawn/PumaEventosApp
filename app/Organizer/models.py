import django
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from User.models import User
from composite_field import CompositeField
# Create your models here.

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=255)


class Evento(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    direccion = models.TextField()
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    capacidad = models.IntegerField()
    etiqueta = models.ManyToManyField(Etiqueta)
    organizador = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
    #periodicidad =



class Invitacion(models.Model):
    evento_id = models.ForeignKey(Evento, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    activa = models.BooleanField()
    asistencia_activa = models.BooleanField()
    id = CompositeField(evento_id,User_id, primary_key=True)
    #codigo_qr ......

class Staff(models.Model):
    user_id = models.ManyToManyField(User)
    evento_id = models.ManyToManyField(Evento)
    staff_id = models.OneToOneField(User, on_delete=models.CASCADE,
                                    parent_link=True)

class ValidaInvitacion(models.Model):
    user_id = models.ForeignKey(Staff)
    invitacion_id = models.ForeignKey(Invitacion)
    id = models.CompositeField(User_id,invitacion_id, primary_key=True)    
