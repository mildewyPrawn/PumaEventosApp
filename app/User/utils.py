from django.contrib.auth.password_validation  import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.utils.translation import ngettext

class IsNotAuthenticatedMixin:
    """
    Pregunta si ya está registrado
    """
    redirect_url = "/"
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(self.redirect_url)

class TamMinContrasena(MinimumLengthValidator):
    """
    Verifica el tamaño de la contraseña
    """
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "La contraseña es muy corta. Esta debe conterner un minimo de %(min_length)d caracter.",
                    "La contraseña es muy corta. Esta debe conterner un minimo de %(min_length)d caracteres.",
                    self.min_length
                ),
                code="password_too_short",
                params={'min_length': self.min_length}
            )
    
    def get_help_text(self):
        return ngettext(
            "Su contraseña debe tener al menos %(min_length)d caracter",
            "Su contraseña debe tener al menos %(min_length)d caracteres",
            self.min_length
        ) % {'min_length': self.min_length}
