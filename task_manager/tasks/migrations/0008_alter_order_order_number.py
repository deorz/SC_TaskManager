# Generated by Django 4.0.4 on 2022-06-03 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_task_running_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.PositiveIntegerField(verbose_name='Номер в очереди'),
        ),
    ]
