# Generated by Django 3.1.1 on 2020-12-16 14:37

from django.db import migrations, models
import testing_system.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('testing_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='is_shown',
            field=models.BooleanField(default=False, verbose_name='Отображать курс для всех?'),
        ),
        migrations.AlterField(
            model_name='studentcodemodel',
            name='code_text',
            field=models.TextField(blank=True, db_index=True, max_length=1000, verbose_name='Введите свое решение здесь'),
        ),
        migrations.AlterField(
            model_name='studentcodemodel',
            name='file',
            field=models.FileField(blank=True, upload_to=testing_system.utilities.user_directory_path, verbose_name='Или отправьте свое решение в виде файла'),
        ),
        migrations.AlterField(
            model_name='task',
            name='memory_limit',
            field=models.PositiveIntegerField(verbose_name='Максимальное количество памяти для программы(в мегабайтах)'),
        ),
    ]
