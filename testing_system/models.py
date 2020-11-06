import json
from datetime import datetime
from os.path import splitext
from pathlib import Path

from django.db import models
from django.urls import reverse
import os

from main.models import Teacher, Student


def user_directory_path(instance, filename):
    """Создает путь к папке ответа ученика"""
    # Костыль с определением типа файла
    return f'answers/{instance.student.username}_{"_".join(instance.task.title.split())}/student_answer_{datetime.now().timestamp()}.{filename.split(".")[-1]}'


# Testing system
class Task(models.Model):
    """The task that the teacher created"""
    title = models.CharField(max_length=100, verbose_name='Название задания',
                             help_text='Название задания')                                                              # Добавить уникаольность
    task_text = models.TextField(max_length=1000, db_index=True, verbose_name='Описание самого задания',
                                 help_text='Текст задания')
    date_publish = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания задания')

    # Приблизительный формат ввода данных, в будущем возможно нужно будет заменить на отдельные модели
    required_form = models.TextField(max_length=1000, db_index=True, verbose_name='Шаблон класса, который задал учител',
                                     help_text='Шаблон формы учителя')
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE, verbose_name='Учитель, который приудмал это задание')

    def save(self, *args, **kwargs):
        try:
            os.mkdir(f'documents/tests/{"_".join(self.title.split())}')
        except OSError:
            pass

        try:
            os.mkdir(f'documents/required_forms/{"_".join(self.title.split())}')
        except OSError:
            pass

        super().save(*args, **kwargs)
        with open(f'documents/tests/{"_".join(self.title.split())}/tests.json', 'w') as f:
            json.dump({}, f)


        with open(f'documents/required_forms/{"_".join(self.title.split())}/required_form.java', 'w') as f1:
            f1.write(self.required_form)

    def get_absolute_url(self):
        return reverse('testing_system:detail_url', args=[self.pk])

    def __str__(self):
        return f'"{self.title}" by {self.teacher.username}'

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        ordering = ['-date_publish']


class StudentCodeModel(models.Model):
    """Модель кода, который отправит ученик, как решение задания"""
    file = models.FileField(upload_to=user_directory_path, blank=True, verbose_name='Загрузка решения')
    code_text = models.TextField(max_length=1000, blank=True, db_index=True, verbose_name='Решение ученика ввиде кода')
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, verbose_name='Ученик')
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE, verbose_name='Задание на которое был отправлен ответ')
    dispatch_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата отправки ответа')

    def save(self, *args, **kwargs):
        path = f'documents/answers/{self.student.username}_{"_".join(self.task.title.split())}/student_answer_{datetime.now().timestamp()}.java'
        if self.code_text != '' and not self.file:
            try:
                os.mkdir(f'documents/answers/{self.student.username}_{"_".join(self.task.title.split())}')
            except OSError:
                pass

            # Поправить костыль с именем path
            with open(path, 'w') as f:
                f.write(self.code_text)
            self.file = f'answers/{self.student.username}_{"_".join(self.task.title.split())}/student_answer_{datetime.now().timestamp()}.java'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Solve {self.task.teacher.username}'s '{self.task.title}' task by {self.student.username}"

    class Meta:
        verbose_name = "Модель ответа ученика"
        verbose_name_plural = "Модели ответов учеников"


class Test(models.Model):
    input = models.CharField(max_length=200, db_index=True, verbose_name='Данные на вход', help_text='Входные данные')
    output = models.CharField(max_length=200, db_index=True, verbose_name='Данные на выход', help_text='Полученные данные')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задание')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # with open(path, 'a') as f:
        #     json.dump(data, f)
        #     f.write('\n')

        path = Path(f'documents/tests/{"_".join(self.task.title.split())}/tests.json')
        with open(path) as f:
            data = json.load(f)
        data[f'{self.pk}'] = {"input": self.input, "output": self.output}
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def __str__(self):
        return f"{self.task.title}'s test"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'