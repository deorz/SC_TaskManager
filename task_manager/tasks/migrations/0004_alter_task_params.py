# Generated by Django 4.0.4 on 2022-06-01 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_status_status_alter_task_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='params',
            field=models.CharField(blank=True, max_length=200, verbose_name='Параметры запуска'),
        ),
    ]
