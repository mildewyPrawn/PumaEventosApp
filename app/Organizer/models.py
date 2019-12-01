import django
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User as UserDjango
from User.models import User
#from compositefk.fields import CompositeForeignKey, LocalFieldValue

# Create your models here.

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return str(self.nombre)


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

    def __str__(self):
        return str(self.nombre) + ': ' + str(self.fecha_inicio)



class Invitacion(models.Model):
    evento_id = models.ForeignKey(Evento, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    activa = models.BooleanField() # True si aún no se lee en el evento
    asistencia_activa = models.BooleanField() # True si ya se leyó en el evento
    qr = models.ImageField(upload_to='images/', blank=True, null=True)
    #id = CompositeForeignKey(id,on_delete=models.CASCADE,to_fields={"evento_id","user_id"})

    class Meta:
        unique_together = (('evento_id', 'user_id'),)
    #codigo_qr ......

    def __str__(self):
        return str(self.evento_id) + '--' + str(self.user_id)

class Staff(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name="staffs")
    evento_id = models.ForeignKey(Evento,on_delete=models.CASCADE)

class ValidaInvitacion(models.Model):
    user_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    invitacion_id = models.ForeignKey(Invitacion,on_delete=models.CASCADE)
    class Meta:
        unique_together = (('user_id', 'invitacion_id'),)    
