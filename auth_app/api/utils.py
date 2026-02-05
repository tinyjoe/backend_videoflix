from email.mime.image import MIMEImage
from pathlib import Path
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .mail_templates import activation_mail_html, activation_mail_text, reset_mail_html, reset_mail_text


def send_activation_email(user, token):
    """
    The function `send_activation_email` sends an activation email to a user with a unique activation
    link.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"{settings.FRONTEND_URL}/pages/auth/activate.html?uid={uidb64}&token={token}"
    subject = 'Activate your Videoflix account'
    text_content = activation_mail_text(user, activation_link)
    html_content = activation_mail_html(user, activation_link)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.attach_alternative(html_content, 'text/html')
    add_inline_logo(email)
    email.send()


def send_password_reset_email(user, token):
    """
    The function `send_password_reset_email` sends a password reset email to a user with a unique token
    and a link to reset the password.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/pages/auth/confirm_password.html?uid={uidb64}&token={token}"
    subject = 'Reset your Videoflix password'
    text_content = reset_mail_text(reset_link)
    html_content = reset_mail_html(reset_link)
    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email],)
    email.attach_alternative(html_content, 'text/html')
    add_inline_logo(email)
    email.send()


def add_inline_logo(email):
    """
    The function `add_inline_logo` attaches an inline logo image to an email for branding purposes.
    """
    logo_path = Path(settings.BASE_DIR) / 'assets' / 'logo_icon.png'
    with open(logo_path, 'rb') as f:
        img = MIMEImage(f.read(), _subtype='png')
        img.add_header('Content-ID', '<videoflix_logo>')
        img.add_header('Content-Disposition', 'inline', filename='logo_icon.png')
        email.attach(img)