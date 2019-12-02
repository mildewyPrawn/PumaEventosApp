from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils import six
import qrcode

def send_email(to_email, subject, content):
    """
    Sends email
    """
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, content, email_from, to_email)

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Genera tokens para mandar invitaciones
    """
    def _make_hash_value(self, inv, timestamp):
        return (
            six.text_type(inv.pk) + six.text_type(timestamp) +
            six.text_type(inv.activa)
        )
# Token generado
invitacion_activacion_token = TokenGenerator()

def make_qr(cadena):
    """
    Crea el código qr y regresa la imagen
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=5,
        border=2)
    qr.add_data(cadena)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    return img
