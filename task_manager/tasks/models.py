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


class System(models.Model):
    available_threads = models.PositiveIntegerField(
        _('Общее количество ядер системы')
    )
    active = models.BooleanField(_('Состояние машины'))


class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
    )
    running_on = models.ForeignKey(
        System,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        verbose_name=_('Исполняется на')
    )
    path = models.CharField(
        _('Путь к исполняемому файлу'), max_length=200
    )
    params = models.CharField(
        _('Параметры запуска'), max_length=200, blank=True
    )
    num_threads = models.PositiveIntegerField(
        _('Количество ядер исполнения'),
    )
    priority = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)],
        default=1
    )

    def __str__(self):
        return f'{self.id}, {self.user}, {self.priority}'


class Order(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_('Задача'),
    )
    order_number = models.PositiveIntegerField(
        _('Номер в очереди'),
    )


class Status(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_('Задача'),
    )
    status = models.CharField(
        _('Статус выполнения'),
        choices=CHOICES,
        max_length=50,
        default='in_queue'
    )

    def __str__(self):
        return self.status
