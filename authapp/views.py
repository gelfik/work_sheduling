# from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect
# from django.template.context_processors import csrf
# from django.contrib.auth.models import User, Group
# from django.contrib import auth
# from .forms import *
from work_sheduling.settings import PASS_SYMBOL_COUNT
from mainapp.views import *
# from django.urls import reverse

def gen_one_password(lenght):
    if lenght <= 8:
        x = 1
    elif 8 < lenght <= 12:
        x = 2
    else:
        x = 3
    import random, string
    Pass_Symbol = []
    spec_cymbol = []
    result = []
    spec_cymbol.extend(list("!#$%&()*+-<=>?"))
    Pass_Symbol.extend(list(string.ascii_letters + string.digits))
    psw = ''.join([random.choice(Pass_Symbol) for x in range(int(lenght - x))]) + ''.join(
        [random.choice(spec_cymbol) for x in range(int(x))])
    result.extend(list(psw))
    random.shuffle(result)
    return "".join(result)


def transliterate(name):
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e', '—': ''}
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


# Create your views here.
def login(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userdata = auth.authenticate(username=username, password=password)
        try:
            usersearch = User.objects.get(username=username)
        except:
            usersearch = None
        if userdata is not None:
            auth.login(request, userdata)
            return redirect('/')
        elif usersearch is not None:
            arguments.update(login_error='Не верный пароль!')
            return render(request, 'authapp/index.html', {'arguments': arguments})
        else:
            arguments.update(login_error='Пользователь не найден!')
            return render(request, 'authapp/index.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.user.is_authenticated and has_group(request.user, 'Руководитель'):
        if request.method == 'POST':
            newuser_form = UserAddForm(request.POST)
            if newuser_form.is_valid():
                new_password = gen_one_password(PASS_SYMBOL_COUNT)
                new_username = transliterate(
                    newuser_form.cleaned_data.get('first_name')[:1] + newuser_form.cleaned_data.get('last_name'))
                user_in_bd = True
                count = 1
                while user_in_bd:
                    if count == 1 and not User.objects.filter(username=new_username).exists():
                        user_in_bd = False
                    elif not User.objects.filter(username=f'{new_username}{count}').exists():
                        user_in_bd = False
                        new_username = f'{new_username}{count}'
                    else:
                        count += 1
                userform = newuser_form.save(username=new_username, password=new_password)
                userform.refresh_from_db()
                userform.last_name = newuser_form.cleaned_data.get('last_name')
                userform.first_name = newuser_form.cleaned_data.get('first_name')
                userform.email = newuser_form.cleaned_data.get('email')
                userform.groups.clear()
                userform.groups.add(newuser_form.cleaned_data.get('group_data'))
                userform.set_password(new_password)
                userform.save()
                usr.set_register(new_username,new_password)
                return redirect(reverse('userlist_url'))
            else:
                usr.set_error('Форма добавления сотрудника заполнена не корректно!')
                return redirect(reverse('userlist_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')

def edit(request, user_id):
    arguments = {}
    arguments.update(csrf(request))
    arguments.update(form=UserAddForm)
    if request.user.is_authenticated and has_group(request.user, 'Руководитель'):
        if request.method == 'GET':
            try:
                user_object = User.objects.get(id=user_id)
                user_object.is_active = 0
                user_object.save()
                return redirect(reverse('userlist_url'))
            except:
                usr.set_error('Сотрудник не найден!')
                return redirect(reverse('userlist_url'))
        elif request.method == 'POST':
            newuser_form = UserAddForm(request.POST)
            if newuser_form.is_valid():
                try:
                    user_object = User.objects.get(id=user_id)
                    user_object.email = newuser_form.cleaned_data.get('email')
                    user_object.last_name = newuser_form.cleaned_data.get('last_name')
                    user_object.first_name = newuser_form.cleaned_data.get('first_name')
                    user_object.groups.clear()
                    user_object.groups.add(newuser_form.cleaned_data.get('group_data'))
                    user_object.save()
                    return redirect(reverse('userlist_url'))
                except:
                    usr.set_error('Сотрудник не найден!')
                    return redirect(reverse('userlist_url'))
            else:
                usr.set_error('Форма редактирвоания сотрудника заполнена не корректно!')
                return redirect(reverse('userlist_url'))
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    else:
        return redirect('/')