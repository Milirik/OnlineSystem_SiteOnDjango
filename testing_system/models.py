from django.db import models
from main.models import Teacher


# Testing system
class Task(models.Model):
    """The task that the teacher created"""
    title = models.CharField(max_length=100, verbose_name='Название задания')
    task_text = models.TextField(max_length=1000, db_index=True, verbose_name='Описание самого задания')

    # Приблизительный формат ввода данных, в будущем возможно нужно будет заменить на отдельные модели
    tests = models.TextField(max_length=1000, db_index=True, verbose_name='Тесты')
    required_form = models.TextField(max_length=1000, db_index=True, verbose_name='Шаблон класса')

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель, который приудмал это задание')
    date_publish = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания задания')

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
