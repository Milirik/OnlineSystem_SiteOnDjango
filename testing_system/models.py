import json
import pika
import os
from datetime import datetime
import time
from pathlib import Path


from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
from django.core.paginator import Paginator

from main.models import Teacher, Student


def user_directory_path(instance, filename):
    """Создает путь к папке ответа ученика"""
    # Костыль с определением типа файла
    return f'answers/{instance.student.username}_{"_".join(instance.task.title.split())}/student_answer_{datetime.now().timestamp()}.{filename.split(".")[-1]}'
    #return f'answers/{instance.student.username}_{"_".join(instance.task.title.split())}/student_answer_{datetime.now().timestamp()}'


# Testing system
class Task(models.Model):
    """The task that the teacher created"""
    title = models.CharField(max_length=100, verbose_name='Название задания',
                             help_text='Название задания')                                                              # Добавить уникальность
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
            json.dump([], f)

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
    status = models.CharField(max_length=100, verbose_name='Статус ответа',
                             help_text='Статус ответа')

    def save(self, *args, **kwargs):
        if not self.file:
            self.file = f'answers/{self.student.username}_{"_".join(self.task.title.split())}/student_answer_{int(round(time.time()*1000))}.java'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Solve {self.task.teacher.username}'s '{self.task.title}' task by {self.student.username}"

    class Meta:
        verbose_name = "Модель ответа ученика"
        verbose_name_plural = "Модели ответов учеников"
        ordering = ['-dispatch_time']


class Test(models.Model):
    input = models.CharField(max_length=200, db_index=True, verbose_name='Данные на вход', help_text='Входные данные')
    output = models.CharField(max_length=200, db_index=True, verbose_name='Данные на выход', help_text='Полученные данные')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задание')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        path = Path(f'documents/tests/{"_".join(self.task.title.split())}/tests.json')
        try:
            data = json.load(open(path))
        except:
            data = []
        data.append({"input": self.input, "output": self.output})

        with open(path, 'w') as f1:
            json.dump(data, f1, ensure_ascii=False, indent=4)

    def __str__(self):
        return f"{self.task.title}'s test"

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


@receiver(post_save, sender=StudentCodeModel)
def answer_saved(sender, instance, **kwargs):
    path = f'documents/{instance.file}'
    try:
        with open(f'documents/{instance.file}', 'r') as fr:
            pass
        os.remove(f'documents/{instance.file}')
    except FileNotFoundError:
        if instance.code_text != '':
            try:
                os.mkdir(f'documents/answers/{instance.student.username}_{"_".join(instance.task.title.split())}')
            except OSError:
                pass

            with open(path, 'w') as f:
                f.write(instance.code_text)
        print(f" [x] Был сохранен ответ с номером - {instance.pk}")
        path_rf = f'OnlineSystem_SiteOnDjango/documents/required_forms/{"_".join(instance.task.title.split())}/required_form.java'
        path_t = f'C:/Users/Кирилл/Desktop/Git/OnlineSystem_SiteOnDjango/documents/tests/{"_".join(instance.task.title.split())}/tests.json'

        all_paths = {
            'student_answer': f'C:/Users/Кирилл/Desktop/Git/OnlineSystem_SiteOnDjango/documents/{f"{instance.file}".split(".")[0]}',
            'required_form': f'{path_rf}',
            'tests': f'{path_t}',
            'answer_id': f'{instance.pk}',
        }

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        channel = connection.channel()
        channel.queue_declare(queue='site_messages')
        channel.basic_publish(exchange='',
                              routing_key='site_messages',
                              body=f'{all_paths}',
                              )
        print(' [x] Sent path.')
        connection.close()


