from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from .forms import *
from django.template.context_processors import csrf
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.utils import timezone

from authapp.forms import *
from .forms import *
from .models import *
from django.urls import reverse
from django.db.models import Q


def has_group(user, group_name):
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


class User_data:
    error_message = ''
    error_status = False
    user = None
    register_login = ''
    register_password = ''
    register_status = False

    def __init__(self):
        self.user = None

    def set_user(self, user):
        self.user = user

    def set_error(self, error_message):
        self.error_message = error_message
        self.error_status = True

    def set_register(self, register_login, register_password):
        self.register_login = register_login
        self.register_password = register_password
        self.register_status = True

    def get_error(self):
        self.error_status = False
        return f'{self.error_message}'

    def get_error_status(self):
        return self.error_status

    def get_register(self):
        self.register_status = False
        return f'{self.register_login}', f'{self.register_password}'

    def get_register_status(self):
        return self.register_status


usr = User_data()


def profile_view(request):
    arguments = {}
    arguments.update()
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'mainapp/profile.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')


def index(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.method == "GET":
        if request.user.is_authenticated:
            if has_group(request.user, 'Сотрудник'):
                return redirect(reverse('sotr_tasklist_url'))
            elif has_group(request.user, 'Руководитель'):
                return redirect(reverse('worklist_url'))
            else:
                auth.logout(request)
                return redirect('/')
        else:
            response = render(request, 'authapp/index.html')
            return response
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


def userlist_view(request):
    arguments = {}
    arguments.update()
    arguments.update(form=UserAddForm)
    arguments.update(user_list=User.objects.filter(is_active=1).order_by('-last_name').order_by('-first_name'))
    user_edit = []
    for i, item in enumerate(arguments['user_list']):
        user_edit.append({'form': UserAddForm(instance=item), 'id': item.id})
    arguments.update(user_edit=user_edit)
    if request.user.is_authenticated and has_group(request.user, 'Руководитель'):
        if request.method == "GET":
            if usr.get_register_status():
                new_username, new_password = usr.get_register()
                arguments.update(add_user_data={'password': new_password, 'username': new_username})
            if usr.get_error_status():
                arguments.update(error=usr.get_error())
            return render(request, 'mainapp/ruc/users_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')


def worklist_view(request):
    arguments = {}
    arguments.update()
    if request.user.is_authenticated and has_group(request.user, 'Руководитель'):
        if request.method == "GET":
            arguments.update(form=work_Form)
            arguments.update(
                work_list=work.objects.filter(del_status=1).filter(
                    (Q(user_id=request.user) | Q(status_id__name='Создано'))).order_by('date_execution', 'date_create'))
            if usr.get_error_status():
                arguments.update(error=usr.get_error())
            return render(request, 'mainapp/ruc/work_list.html', {'arguments': arguments})
        elif request.method == "POST":
            new_form = work_Form(request.POST)
            if new_form.is_valid():
                new_work = new_form.save(user_data=request.user)
                new_work.save()
                return redirect(reverse('tasklist_url', args=[new_work.id]))
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=new_form)
                return render(request, 'mainapp/ruc/work_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')


def worklist_update_view(request, work_id):
    arguments = {}
    arguments.update()
    if request.user.is_authenticated and has_group(request.user, 'Руководитель'):
        if request.method == "GET":
            try:
                work_object = work.objects.get(id=work_id)
                work_object.del_status = 0
                work_object.save()
                return redirect(reverse('worklist_url'))
            except:
                usr.set_error('Работа не найдена!')
                return redirect(reverse('worklist_url'))
        elif request.method == "POST":
            work_form = work_Form(request.POST)
            if work_form.is_valid():
                try:
                    work_object = work.objects.get(id=work_id, del_status=1)
                    work_object.name = work_form.cleaned_data.get('name')
                    work_object.status_id = work_form.cleaned_data.get('status_id')
                    work_object.date_execution = work_form.cleaned_data.get('date_execution')
                    work_object.save()
                    return redirect(reverse('tasklist_url', args=[work_id]))
                except Exception as e:
                    print(e)
                    usr.set_error('Работа не найдена!')
                    return redirect(reverse('tasklist_url', args=[work_id]))
            else:
                usr.set_error('Форма редактирвоания работы заполнена не корректно!')
                return redirect(reverse('tasklist_url', args=[work_id]))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')


def tasklist_view(request, work_id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Руководитель'):
        if request.method == "GET":
            try:
                work_object = work.objects.get(id=work_id, del_status=1)
                arguments.update(form=task_Form)
                arguments.update(work=work_object)
                arguments.update(form_work=work_Form(instance=work_object))
                arguments.update(
                    task_list=tasks.objects.filter(del_status=1, work_id=work_id).order_by('-date_execution',
                                                                                           '-date_create'))
                task_edit = []
                for i, item in enumerate(arguments['task_list']):
                    task_edit.append({'form': task_Form(instance=item), 'id': item.id})
                arguments.update(task_edit=task_edit)
            except Exception as e:
                print(e)
                arguments.update(error='Работа не найдена!')
            if usr.get_error_status():
                arguments.update(error=usr.get_error())
            return render(request, 'mainapp/ruc/task_list.html', {'arguments': arguments})
        elif request.method == "POST":
            new_form = task_Form(request.POST)
            if new_form.is_valid():
                if new_form.cleaned_data.get('date_execution') >= timezone.now().date():
                    work_object = work.objects.get(id=work_id)
                    new_task = new_form.save(user_data=new_form.cleaned_data.get('user_id'), work_data=work_object)
                    new_task.save()
                    if work_object.date_execution <= new_task.date_execution:
                        work_object.date_execution = new_task.date_execution
                        work_object.save()
                else:
                    usr.set_error('Вы не можете создать задание, со сроком выполнения прошлой датой!')
                return redirect(reverse('tasklist_url', args=[work_id]))
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=new_form)
                return render(request, 'mainapp/ruc/work_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')


def tasklist_update_view(request, work_id, task_id):
    arguments = {}
    arguments.update(form=task_Form)
    if request.user.is_authenticated and has_group(request.user, 'Руководитель'):
        if request.method == "GET":
            try:
                tasks_object = tasks.objects.get(id=task_id)
                tasks_object.del_status = 0
                tasks_object.save()
                return redirect(reverse('tasklist_url', args=[work_id]))
            except:
                usr.set_error('Задание не найдено!')
                return redirect(reverse('tasklist_url', args=[work_id]))
        elif request.method == "POST":
            tasks_object = tasks.objects.get(id=task_id, del_status=1)
            task_form = task_Form(request.POST, instance=tasks_object)
            if task_form.is_valid():
                try:
                    tasks_object.save()
                    return redirect(reverse('tasklist_url', args=[work_id]))
                except Exception as e:
                    print(e)
                    usr.set_error('Задание не найдено!')
                    return redirect(reverse('tasklist_url', args=[work_id]))
            else:
                usr.set_error('Форма редактирвоания задания заполнена не корректно!')
                return redirect(reverse('tasklist_url', args=[work_id]))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')


def sotr_tasklist_view(request):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Сотрудник'):
        if request.method == "GET":
            try:
                arguments.update(
                    task_list=tasks.objects.filter(del_status=1, user_id=request.user).order_by('-date_execution',
                                                                                                '-date_create'))
                task_edit = []
                for i, item in enumerate(arguments['task_list']):
                    task_edit.append({'form': sotr_task_Form(instance=item), 'id': item.id})
                arguments.update(task_edit=task_edit)
            except Exception as e:
                print(e)
                arguments.update(error='Работа не найдена!')
            if usr.get_error_status():
                arguments.update(error=usr.get_error())
            return render(request, 'mainapp/sotr/task_list.html', {'arguments': arguments})
        elif request.method == "POST":
            new_form = task_Form(request.POST)
            if new_form.is_valid():
                if new_form.cleaned_data.get('date_execution') >= timezone.now().date():
                    work_object = work.objects.get()
                    new_task = new_form.save(user_data=new_form.cleaned_data.get('user_id'), work_data=work_object)
                    new_task.save()
                    if work_object.date_execution <= new_task.date_execution:
                        work_object.date_execution = new_task.date_execution
                        work_object.save()
                else:
                    usr.set_error('Вы не можете создать задание, со сроком выполнения прошлой датой!')
                return redirect(reverse('tasklist_url', args=[]))
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=new_form)
                return render(request, 'mainapp/ruc/work_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')
