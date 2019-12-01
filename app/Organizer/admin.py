from django.contrib import admin
from .models import Evento, Etiqueta, Staff, Invitacion


# Register your models here.
admin.site.register(Evento)
admin.site.register(Etiqueta)
admin.site.register(Staff)
admin.site.register(Invitacion)

#admin.site.register()