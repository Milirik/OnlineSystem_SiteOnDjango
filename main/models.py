from django.db import models
from django.contrib.auth.models import AbstractUser


# Users
class Student(AbstractUser):
    """Model for new people and students"""

    class Meta(AbstractUser.Meta):
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class Teacher(Student):
    """Model for teachers who will create tasks"""
    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


# Tasks
class Task(models.Model):
    title = models.CharField(max_length=100)
