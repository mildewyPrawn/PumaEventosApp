from django.contrib import admin
<<<<<<< HEAD
from .models import Usuario

# Register your models here.
admin.site.register(Usuario)
=======
from .models import User, AcademicEntity

# Register your models here.
admin.site.register(User)
admin.site.register(AcademicEntity)
>>>>>>> 6d07c76eb2be07748ee1f6eba56a692c67591e16
