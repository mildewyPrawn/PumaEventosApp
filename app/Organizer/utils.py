"""Utils"""

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

def send_email(to_email, subject, content):
    """
    Sends email
    """
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, content, email_from, to_email)

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, inv, timestamp):
        return (
            six.text_type(inv.pk) + six.text_type(timestamp) +
            six.text_type(inv.activa)
        )
invitacion_activacion_token = TokenGenerator()
