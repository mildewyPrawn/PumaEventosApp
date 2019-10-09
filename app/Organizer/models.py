import django
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from User.models import Usuario
# Create your models here.

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
    organizador = models.OneToOneField(Usuario, on_delete=models.CASCADE, parent_link=True)
    #periodicidad =

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=255)


class Invitacion(models.Model):
    evento_id = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario_id = models.ForeignKey(Usuario)
    activa = models.BooleanField()
    asistencia_activa = models.BooleanField()
    id = models.CompositeField(evento_id,usuario_id, primary_key=True)
    #codigo_qr ......

class Staff(models.Model):
    usuario_id = models.ManyToManyField(Usuario)
    evento_id = models.ManyToManyField(Evento)
    staff_id = models.OneToOneField(Usuario, on_delete=models.CASCADE,
                                    parent_link=True)

class ValidaInvitacion(models.Model):
    usuario_id = models.ForeignKey(Staff)
    invitacion_id = models.ForeignKey(Invitacion)
    id = models.CompositeField(usuario_id,invitacion_id, primary_key=True)    
