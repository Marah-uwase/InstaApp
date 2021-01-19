from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_


def send_activation_email(user, current_site, receiver):
    subject = 'Activate your account'

    message = render_to_string('registration/activate.html', {
        'user':user,
        'domain':current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        
    })

    email = EmailMessage(subject, message, to=[receiver])
    email.send()