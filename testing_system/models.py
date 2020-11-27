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


from main.models import Teacher, Student


def user_directory_path(instance, filename):
    """Создает путь к папке ответа ученика"""
    # Костыль с определением типа файла
    return f'answers/{instance.student.username}_{"_".join(instance.task.title.split())}/{int(round(time.time()*1000))}' \
           f'/{filename}'


# Testing system
class Task(models.Model):
    """The task that the teacher created"""
    title = models.CharField(max_length=100, verbose_name='Название задания',
                             help_text='Название задания', unique=True)

    task_text = models.TextField(max_length=1000, db_index=True, verbose_name='Описание самого задания',
                                 help_text='Текст задания')

    name_class = models.CharField(max_length=100, verbose_name='Название класса программы',
                                  help_text='Название класса программы', default="ReqForm")

    date_publish = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания задания')

    required_form = models.TextField(max_length=1000, db_index=True, verbose_name='Необходимый шаблон класса',
                                     help_text='Шаблон формы учителя')
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE,
                                verbose_name='Учитель, который приудмал это задание')

    time_limit = models.PositiveIntegerField(verbose_name='Максимальное время выполнения программы(в милисекундах)')
    memory_limit = models.PositiveIntegerField(verbose_name='Максимальное количество памяти для программы(в байтах)')

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

        with open(f'documents/required_forms/{"_".join(self.title.split())}/{self.name_class}.java', 'w') as f1:
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
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE,
                             verbose_name='Задание на которое был отправлен ответ')
    dispatch_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата отправки ответа')
    status = models.CharField(max_length=1000, verbose_name='Статус ответа', help_text='Статус ответа',
                              default='Проверяется')

    def save(self, *args, **kwargs):
        if self.status != "В очереди":
            # Чистка директорий от файлов
            os.remove(f'documents/{self.file}')                                                                         # Не удаляется временная папка
            # os.remove(f'documents/answers/{str(self.file).split("/")[-3]+"/"+str(self.file).split("/")[-2]}')

        else:
            if not self.file:
                time_ = int(round(time.time()*1000))
                self.file = f'answers/{self.student.username}_{"_".join(self.task.title.split())}/{time_}/{self.task.name_class}.java'
                try:
                    os.mkdir(f'documents/answers/{self.student.username}_{"_".join(self.task.title.split())}')
                except OSError:
                    pass
                try:
                    os.mkdir(f'documents/answers/{self.student.username}_{"_".join(self.task.title.split())}/{time_}')
                except OSError:
                    pass

                with open(f'documents/{self.file}', 'w') as f:
                    f.write(self.code_text)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Solve {self.task.teacher.username}'s '{self.task.title}' task by {self.student.username}"

    class Meta:
        verbose_name = "Модель ответа ученика"
        verbose_name_plural = "Модели ответов учеников"
        ordering = ['-dispatch_time']


class Test(models.Model):
    input = models.CharField(max_length=200, db_index=True, verbose_name='Данные на вход', help_text='Входные данные')
    output = models.CharField(max_length=200, db_index=True, verbose_name='Данные на выход',
                              help_text='Полученные данные')
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
    if instance.status == "В очереди":
        all_paths = {
            "student_answer": f'C:/Users/Кирилл/Desktop/Git/OnlineSystem_SiteOnDjango/documents/'
                              f'{f"{instance.file}".split(".")[0]}',                                                        # Расширение не отправляется
            "required_form": f'C:/Users/Кирилл/Desktop/Git/OnlineSystem_SiteOnDjango/documents/required_forms/'
                             f'{"_".join(instance.task.title.split())}/{instance.task.name_class}.java',
            "tests": f'C:/Users/Кирилл/Desktop/Git/OnlineSystem_SiteOnDjango/documents/tests/'
                     f'{"_".join(instance.task.title.split())}/tests.json',
            "time_limit": instance.task.time_limit,
            "memory_limit": instance.task.memory_limit,
            "answer_id": {instance.pk},
        }

        print(f" [x] Был сохранен ответ с номером - {instance.pk}")

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
