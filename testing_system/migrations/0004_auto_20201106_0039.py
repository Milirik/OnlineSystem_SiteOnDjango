# Generated by Django 3.1.1 on 2020-11-05 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_delete_task'),
        ('testing_system', '0003_auto_20201104_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.teacher', verbose_name='Учитель, который приудмал это задание'),
        ),
    ]