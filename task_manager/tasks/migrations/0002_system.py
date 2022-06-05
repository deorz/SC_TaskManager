# Generated by Django 4.0.4 on 2022-06-01 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_threads', models.PositiveIntegerField(verbose_name='Общее количество ядер системы')),
                ('active', models.BooleanField(verbose_name='Состояние машины')),
            ],
        ),
    ]
