from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_activation_email(user, token):
    """
    The function `send_activation_email` sends an activation email to a user with a unique activation
    link.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"http://localhost:8000/api/activate/{uidb64}/{token}/"
    subject = 'Activate your Videoflix account'
    text_content = activation_mail_text(user, activation_link)
    html_content = activation_mail_html(user, activation_link)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.attach_alternative(html_content, 'text/html')
    email.send()


def send_password_reset_email(user, token):
    """
    The function `send_password_reset_email` sends a password reset email to a user with a unique token
    and a link to reset the password.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"http://localhost:8000/api/password_confirm/{uidb64}/{token}/"
    subject = 'Reset your Videoflix password'
    text_content = reset_mail_text(user, reset_link)
    html_content = reset_mail_html(user, reset_link)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.attach_alternative(html_content, 'text/html')
    email.send()


def activation_mail_html(user, activation_link):
    """
    The function `activation_mail_html` generates an HTML email template for sending activation links to
    users.
    """
    return f"""
    <p>Hi {user.email},</p>
    <p>Please click the link below to activate your account:</p>
    <p><a href="{activation_link}">Activate your account</a></p>
    <p>Thank you!</p>
    """


def activation_mail_text(user, activation_link):
    """
    The function `activation_mail_text` generates an activation email message with a personalized
    greeting and activation link for a user.
    """
    return f"""
    Hi {user.email},
    Please click the link below to activate your account:
    {activation_link}
    Thank you!
    """


def reset_mail_html(user, reset_link):
    """
    The function `reset_mail_html` generates an HTML email template for resetting a user's password,
    including the user's email and a reset link.
    """
    return f"""
    <p>Hi {user.email},</p>
    <p>Please click the link below to reset your password:</p>
    <p><a href="{reset_link}">Reset your password</a></p>
    <p>Thank you!</p>
    """


def reset_mail_text(user, reset_link):
    """
    The function `reset_mail_text` generates a password reset email message with the user's email and a
    reset link.
    """
    return f"""
    Hi {user.email},
    Please click the link below to reset your password:
    {reset_link}
    Thank you!
    """