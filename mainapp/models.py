from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _

# Create your models here.

class status_list(models.Model):
    name = models.CharField('Наименование', max_length=256, default=None)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        db_table = 'status_list'

    def __str__(self):
        return self.name


class work(models.Model):
    name = models.CharField('Наименование работы', max_length=256, default=None)
    date_create = models.DateField('Дата создания', auto_now_add=True)
    date_execution = models.DateField('Дата выполнения', default=None)
    date_last_edit = models.DateField('Дата последней правки', auto_now=True)
    status_id = models.ForeignKey(status_list, on_delete=models.CASCADE, verbose_name='Статус', default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Исполнитель')
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        db_table = 'works'

    def __str__(self):
        return self.name


class tasks(models.Model):
    name = models.CharField('Наименование задания', max_length=256, default=None)
    result = models.TextField('Результат', default=None, null=True)
    date_create = models.DateField('Дата создания', auto_now_add=True)
    date_execution = models.DateField('Срок исполнения', default=None)
    date_last_edit = models.DateField('Дата последней правки', auto_now=True)
    status_id = models.ForeignKey(status_list, on_delete=models.CASCADE, verbose_name='Статус', default=None)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Исполнитель', null=True, blank=True)
    work_id = models.ForeignKey(work, on_delete=models.CASCADE, verbose_name='Работа', default=None)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Задания'
        verbose_name_plural = 'Задания'
        db_table = 'tasks'

    def __str__(self):
        return self.name