from django.contrib import admin
from .models import *

@admin.register(status_list)
class status_list(admin.ModelAdmin):
    list_display = ('name', 'del_status')

@admin.register(work)
class work(admin.ModelAdmin):
    list_display = ('name', 'date_create', 'date_execution', 'date_last_edit', 'status_id', 'user_id', 'del_status')

@admin.register(tasks)
class tasks(admin.ModelAdmin):
    list_display = ('name', 'work_id', 'date_create', 'date_execution', 'date_last_edit', 'result', 'status_id', 'user_id', 'del_status')