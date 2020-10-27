# Generated by Django 3.1.1 on 2020-10-27 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentCodeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/', verbose_name='Загрузка рещения')),
                ('code_text', models.TextField(db_index=True, max_length=1000, verbose_name='Шаблон класса')),
            ],
            options={
                'verbose_name': 'Модель ответа ученика',
                'verbose_name_plural': 'Модели ответов учеников',
            },
        ),
        migrations.AlterField(
            model_name='task',
            name='required_form',
            field=models.TextField(db_index=True, max_length=1000, verbose_name='Шаблон класса, который задал учител'),
        ),
        migrations.AddField(
            model_name='task',
            name='answer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='testing_system.studentcodemodel', verbose_name='Ответ ученика. Текст или файл'),
        ),
    ]
