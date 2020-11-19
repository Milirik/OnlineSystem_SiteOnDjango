# Generated by Django 3.1.1 on 2020-11-19 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import testing_system.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Название задания', max_length=100, verbose_name='Название задания')),
                ('task_text', models.TextField(db_index=True, help_text='Текст задания', max_length=1000, verbose_name='Описание самого задания')),
                ('date_publish', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания задания')),
                ('required_form', models.TextField(db_index=True, help_text='Шаблон формы учителя', max_length=1000, verbose_name='Шаблон класса, который задал учител')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.teacher', verbose_name='Учитель, который приудмал это задание')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
                'ordering': ['-date_publish'],
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.CharField(db_index=True, help_text='Входные данные', max_length=200, verbose_name='Данные на вход')),
                ('output', models.CharField(db_index=True, help_text='Полученные данные', max_length=200, verbose_name='Данные на выход')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testing_system.task', verbose_name='Задание')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.CreateModel(
            name='StudentCodeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to=testing_system.models.user_directory_path, verbose_name='Загрузка решения')),
                ('code_text', models.TextField(blank=True, db_index=True, max_length=1000, verbose_name='Решение ученика ввиде кода')),
                ('dispatch_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата отправки ответа')),
                ('status', models.CharField(help_text='Статус ответа', max_length=100, verbose_name='Статус ответа')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='testing_system.task', verbose_name='Задание на которое был отправлен ответ')),
            ],
            options={
                'verbose_name': 'Модель ответа ученика',
                'verbose_name_plural': 'Модели ответов учеников',
                'ordering': ['-dispatch_time'],
            },
        ),
    ]
