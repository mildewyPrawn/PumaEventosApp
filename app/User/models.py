import django
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


class Usuario(models.Model):
    nombre = models.CharField(max_length=42)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(max_length=75)
    #contraseña
    #foto

class EntidadAcademica(models.Model):
    nombre = models.CharField(max_length=255)
