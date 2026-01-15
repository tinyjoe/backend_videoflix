from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_activation_email(user, token):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"http://localhost:8000/api/activate/{uidb64}/{token}/"
    subject = "Activate your Videoflix account"
    text_content = activation_mail_text(user, activation_link)
    html_content = activation_mail_html(user, activation_link)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_password_reset_email(user, token):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"http://localhost:8000/api/password_confirm/{uidb64}/{token}/"
    subject = "Reset your Videoflix password"
    text_content = reset_mail_text(user, reset_link)
    html_content = reset_mail_html(user, reset_link)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.attach_alternative(html_content, "text/html")
    email.send()


def activation_mail_html(user, activation_link):
    return f"""
    <p>Hi {user.email},</p>
    <p>Please click the link below to activate your account:</p>
    <p><a href="{activation_link}">Activate your account</a></p>
    <p>Thank you!</p>
    """


def activation_mail_text(user, activation_link):
    return f"""
    Hi {user.email},
    Please click the link below to activate your account:
    {activation_link}
    Thank you!
    """


def reset_mail_html(user, reset_link):
    return f"""
    <p>Hi {user.email},</p>
    <p>Please click the link below to reset your password:</p>
    <p><a href="{reset_link}">Reset your password</a></p>
    <p>Thank you!</p>
    """


def reset_mail_text(user, reset_link):
    return f"""
    Hi {user.email},
    Please click the link below to reset your password:
    {reset_link}
    Thank you!
    """