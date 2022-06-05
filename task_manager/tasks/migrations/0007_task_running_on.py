# Generated by Django 4.0.4 on 2022-06-02 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_status_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='running_on',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.system', verbose_name='Исполняется на'),
        ),
    ]
