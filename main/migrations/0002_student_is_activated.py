# Generated by Django 3.1.1 on 2020-10-25 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_activated',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Прошел активацию?'),
        ),
    ]