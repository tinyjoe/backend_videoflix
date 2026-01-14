from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_activation_email(user, token):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"https://localhost:8000/activate/{uidb64}/{token}/"
    subject = "Activate your Videoflix account"
    message = f"Hi {user.email},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nThank you!"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])