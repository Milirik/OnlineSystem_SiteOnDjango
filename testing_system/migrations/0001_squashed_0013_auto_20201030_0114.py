# Generated by Django 3.1.1 on 2020-10-29 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import testing_system.models


class Migration(migrations.Migration):

    replaces = [('testing_system', '0001_initial'), ('testing_system', '0002_auto_20201027_2306'), ('testing_system', '0003_auto_20201029_2305'), ('testing_system', '0004_auto_20201029_2311'), ('testing_system', '0005_auto_20201029_2321'), ('testing_system', '0006_auto_20201029_2329'), ('testing_system', '0007_auto_20201030_0018'), ('testing_system', '0008_auto_20201030_0022'), ('testing_system', '0009_auto_20201030_0027'), ('testing_system', '0010_auto_20201030_0033'), ('testing_system', '0011_auto_20201030_0033'), ('testing_system', '0012_auto_20201030_0114'), ('testing_system', '0013_auto_20201030_0114')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_delete_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название задания')),
                ('task_text', models.TextField(db_index=True, max_length=1000, verbose_name='Описание самого задания')),
                ('tests', models.TextField(db_index=True, max_length=1000, verbose_name='Тесты')),
                ('required_form', models.TextField(db_index=True, max_length=1000, verbose_name='Шаблон класса, который задал учител')),
                ('date_publish', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания задания')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.teacher', verbose_name='Учитель, который приудмал это задание')),
            ],
            options={
                'verbose_name': 'Задание',
                'verbose_name_plural': 'Задания',
            },
        ),
        migrations.CreateModel(
            name='StudentCodeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to=testing_system.models.user_directory_path, verbose_name='Загрузка рещения')),
                ('code_text', models.TextField(blank=True, db_index=True, max_length=1000, verbose_name='Шаблон класса')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='testing_system.task', verbose_name='Задание на которое был отправлен ответ')),
            ],
            options={
                'verbose_name': 'Модель ответа ученика',
                'verbose_name_plural': 'Модели ответов учеников',
            },
        ),
    ]
