from django.db import models
from django.urls import reverse

from main.models import Teacher, Student


def user_directory_path(instance, filename):
    """Создает путь к папке ответа ученика"""
    # print(dir(instance))
    return f'answers/{instance.student.username}_{instance.task.title[:10]}'


# Testing system
class Task(models.Model):
    """The task that the teacher created"""
    title = models.CharField(max_length=100, verbose_name='Название задания')
    task_text = models.TextField(max_length=1000, db_index=True, verbose_name='Описание самого задания')
    date_publish = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания задания')

    # Приблизительный формат ввода данных, в будущем возможно нужно будет заменить на отдельные модели
    tests = models.TextField(max_length=1000, db_index=True, verbose_name='Тесты')
    required_form = models.TextField(max_length=1000, db_index=True, verbose_name='Шаблон класса, который задал учител')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель, который приудмал это задание')

    def get_absolute_url(self):
        return reverse('testing_system:detail_url', args=[self.pk])

    def __str__(self):
        return f'"{self.title}" by {self.teacher.username}'

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class StudentCodeModel(models.Model):
    """Модель кода, который отправит ученик, как решение задания"""
    file = models.FileField(upload_to=user_directory_path, blank=True, verbose_name='Загрузка решения')
    code_text = models.TextField(max_length=1000, blank=True, db_index=True, verbose_name='Решение ученика ввиде кода')
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, verbose_name='Ученик')
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE, verbose_name='Задание на которое был отправлен ответ')

    def __str__(self):
        return f"Solve {self.task.teacher.username}'s '{self.task.title}' task by {self.student.username}"

    class Meta:
        verbose_name = "Модель ответа ученика"
        verbose_name_plural = "Модели ответов учеников"


# В разработке
# class CheckModel(models.Model):
#     """Сheck cycle. From sending files to getting results."""
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
