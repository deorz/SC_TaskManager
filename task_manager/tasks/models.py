from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()

CHOICES = [
    ('in_queue', 'Поставлена в очередь'),
    ('running', 'Выполняется'),
    ('stopped', 'Приостановлена'),
    ('executed', 'Завершена'),
    ('deleted', 'Удалена')
]


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь')
    )
    path = models.FilePathField(_('Путь к исполняемому файлу'))
    params = models.CharField(_('Параметры запуска'), max_length=200)
    num_threads = models.PositiveIntegerField(_('Количество ядер исполнения'))
    priority = models.PositiveIntegerField(validators=[MaxValueValidator(100)],
                                           )


class Order(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_('Задача')
    )
    order_number = models.PositiveIntegerField(_('Номер в очереди'))


class Status(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_('Задача')
    )
    status = models.CharField(_('Статус выполнения'),
                              choices=CHOICES,
                              max_length=50)
