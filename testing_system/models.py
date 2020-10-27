from django.db import models
from django.urls import reverse

from main.models import Teacher


# Testing system
class StudentCodeModel(models.Model):
    """Модель кода, который отправит ученик, как решение задания"""

    file = models.FileField(upload_to='documents/', blank=True, verbose_name='Загрузка рещения')
    code_text = models.TextField(max_length=1000, blank=True, db_index=True, verbose_name='Шаблон класса')

    class Meta:
        verbose_name = "Модель ответа ученика"
        verbose_name_plural = "Модели ответов учеников"


class Task(models.Model):
    """The task that the teacher created"""
    title = models.CharField(max_length=100, verbose_name='Название задания')
    task_text = models.TextField(max_length=1000, db_index=True, verbose_name='Описание самого задания')
    date_publish = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания задания')

    # Приблизительный формат ввода данных, в будущем возможно нужно будет заменить на отдельные модели
    tests = models.TextField(max_length=1000, db_index=True, verbose_name='Тесты')
    required_form = models.TextField(max_length=1000, db_index=True, verbose_name='Шаблон класса, который задал учител')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель, который приудмал это задание')
    answer = models.ForeignKey(StudentCodeModel, on_delete=models.CASCADE, verbose_name='Ответ ученика. Текст или файл',
                               default=None)

    def get_absolute_url(self):
        return reverse('testing_system:detail_url', args=[self.pk])

    def __str__(self):
        return f'"{self.title}" by {self.teacher.username}'

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


# В разработке
# class CheckModel(models.Model):
#     """Сheck cycle. From sending files to getting results."""
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
