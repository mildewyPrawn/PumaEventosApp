from django.contrib.auth.models import User as UserDjango
from django.db import models
from django.template.defaultfilters import slugify
import django

class User(models.Model):
    first_name = models.CharField(max_length=42, null=False)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=75, null=False)
    user = models.ForeignKey(UserDjango, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    password = models.CharField(max_length=100, null=False)
    staff = models.BooleanField(null=False, default=False)

class AcademicEntity(models.Model):
    nombre = models.CharField(max_length=255)
