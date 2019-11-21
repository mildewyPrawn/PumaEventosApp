from django.contrib import admin
from .models import User, AcademicEntity

# Register your models here.
admin.site.register(User)
admin.site.register(AcademicEntity)