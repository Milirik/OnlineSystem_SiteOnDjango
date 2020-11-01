# Generated by Django 3.1.1 on 2020-11-01 16:41

from django.db import migrations, models
import django.utils.timezone
import testing_system.models


class Migration(migrations.Migration):

    dependencies = [
        ('testing_system', '0001_squashed_0013_auto_20201030_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcodemodel',
            name='dispatch_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now, verbose_name='Дата отправки ответа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentcodemodel',
            name='code_text',
            field=models.TextField(blank=True, db_index=True, max_length=1000, verbose_name='Решение ученика ввиде кода'),
        ),
        migrations.AlterField(
            model_name='studentcodemodel',
            name='file',
            field=models.FileField(blank=True, upload_to=testing_system.models.user_directory_path, verbose_name='Загрузка решения'),
        ),
    ]