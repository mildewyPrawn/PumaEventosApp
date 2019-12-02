from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
import django

class Usuario(models.Model):
    """
    Modelo del usuario
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, default=1)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    es_Organizador = models.BooleanField(default=False)
    es_Staff = models.BooleanField(default=False)
    entidad = models.CharField(max_length=300, null=True)

    def __str__(self):
        return str(self.user)

class AcademicEntity(models.Model):
    """
    Modelo de la entidad académica
    """
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return str(self.nombre)
