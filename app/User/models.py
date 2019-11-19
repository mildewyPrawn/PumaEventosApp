from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
import django

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, default=1)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    #es_Organizador = models.BooleanField(default=False) , default="static/mrX.png"
    #es_Staff = models.BooleanField(default=False)

    #def create_user_Usuario(self, user1, avatar):
    #    user = self.model(user=user1, avatar=avatar)
    #    user.save(using=self._db)
    #    return user

class AcademicEntity(models.Model):
    nombre = models.CharField(max_length=255)
