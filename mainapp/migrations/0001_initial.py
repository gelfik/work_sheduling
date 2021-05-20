# Generated by Django 3.1.2 on 2021-05-18 04:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='status_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=256, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
                'db_table': 'status_list',
            },
        ),
        migrations.CreateModel(
            name='work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=256, verbose_name='Наименование работы')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_execution', models.DateField(default=None, verbose_name='Срок исполнения')),
                ('date_last_edit', models.DateField(auto_now=True, verbose_name='Дата последней правки')),
                ('del_status', models.BooleanField(default=True, verbose_name='Статус удаления')),
                ('status_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.status_list', verbose_name='Статус')),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
            ],
            options={
                'verbose_name': 'Работа',
                'verbose_name_plural': 'Работы',
                'db_table': 'works',
            },
        ),
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=256, verbose_name='Наименование задания')),
                ('result', models.TextField(default=None, verbose_name='Результат')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_execution', models.DateField(default=None, verbose_name='Срок исполнения')),
                ('date_last_edit', models.DateField(auto_now=True, verbose_name='Дата последней правки')),
                ('del_status', models.BooleanField(default=True, verbose_name='Статус удаления')),
                ('status_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.status_list', verbose_name='Статус')),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
                ('work_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.work', verbose_name='Работа')),
            ],
            options={
                'verbose_name': 'Задания',
                'verbose_name_plural': 'Задания',
                'db_table': 'tasks',
            },
        ),
    ]
