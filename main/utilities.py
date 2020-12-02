from django.template.loader import render_to_string
from django.core.signing import Signer
from OnlineSystem_SiteOnDjango.settings import ALLOWED_HOSTS

signer = Signer()


def send_activation_notification(user):
    """ Отправляет письмо с ссылкой на регистрацию нового пользователя"""
    host = 'http://' + ALLOWED_HOSTS[0] if ALLOWED_HOSTS else 'http://localhost:8000'
    context = {
        'user': user,
        'host': host,
        'sign': signer.sign(user.username),
    }
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def user_image_path(instance, filename):
    return f"images/users/{instance.username}_{filename}"
