from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from .utilities import send_activation_notification, user_image_path


# Сигнал об отправки письма регистрации
user_registration = Signal(providing_args=['instance'])


def user_registration_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registration.connect(user_registration_dispatcher)


# Users
class Student(AbstractUser):
    """Model for new people and students"""
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    image = models.ImageField(blank=True, upload_to=user_image_path, verbose_name='Изображение')

    def __str__(self):
        return f'{self.username}'

    class Meta(AbstractUser.Meta):
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(Student):
    """Model for teachers who will create tasks"""

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

