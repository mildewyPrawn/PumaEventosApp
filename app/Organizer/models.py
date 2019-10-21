import django
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as UserDjango
from User.models import User
from compositefk.fields import CompositeForeignKey, LocalFieldValue

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
    organizador = models.ForeignKey(User, on_delete=models.CASCADE)
    #periodicidad =



class Invitacion(models.Model):
    evento_id = models.ForeignKey(Evento, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    activa = models.BooleanField()
    asistencia_activa = models.BooleanField()
    #id = CompositeForeignKey(id,on_delete=models.CASCADE,to_fields={"evento_id","user_id"})

    class Meta:
        unique_together = (('evento_id', 'user_id'),)
    #codigo_qr ......

class Staff(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name="staffs")
    evento_id = models.ForeignKey(Evento,on_delete=models.CASCADE)

class ValidaInvitacion(models.Model):
    user_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    invitacion_id = models.ForeignKey(Invitacion,on_delete=models.CASCADE)
    class Meta:
        unique_together = (('user_id', 'invitacion_id'),)    
