from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext, gettext_lazy as _
from django.forms import ModelForm
from .models import *


class UserFullName(User):
    class Meta:
        proxy = True
        ordering = ["username"]

    def __str__(self):
        return self.get_full_name()


class status_Form(ModelForm):
    name = forms.CharField(label=_("Наименование"), widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = status_list
        fields = ['name']


class work_Form(ModelForm):
    name = forms.CharField(label=_("Наименование"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    status_id = forms.ModelChoiceField(label=_("Статус"), widget=forms.Select(attrs={'class': 'form-control'}),
                                       queryset=None)
    user_id = forms.ModelChoiceField(label=_("Исполнитель"), widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=None, required=False)
    date_execution = forms.DateField(label=_("Дата выполнения"),
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                            format=('%Y-%m-%d')))

    class Meta:
        model = work
        fields = ['name', 'status_id', 'user_id', 'date_execution']

    def __init__(self, *args, **kwargs):
        super(work_Form, self).__init__(*args, **kwargs)
        self.fields['status_id'].queryset = status_list.objects.filter(del_status=1)
        self.fields['user_id'].queryset = UserFullName.objects.filter(is_active=1)
        # del self.fields['user_id']
        # if self.instance and self.instance.pk is None:
        #     del self.fields['status_id']

    def save(self, commit=True, user_data=None):
        data = super(work_Form, self).save(commit=False)
        data.user_id = user_data
        if self.instance and self.instance.pk is None:
            data.status_id = status_list.objects.get(name='Назначено')
        if commit:
            data.save()
        return data


class task_Form(ModelForm):
    name = forms.CharField(label=_("Наименование"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    result = forms.CharField(label=_("Результат"), widget=forms.Textarea(attrs={'class': 'form-control'}),
                             required=False)
    status_id = forms.ModelChoiceField(label=_("Статус"), widget=forms.Select(attrs={'class': 'form-control'}),
                                       queryset=None)
    user_id = forms.ModelChoiceField(label=_("Исполнитель"), widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=None, required=False)
    date_execution = forms.DateField(label=_("Срок выполнения"),
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                            format=('%Y-%m-%d')))

    class Meta:
        model = tasks
        fields = ['name', 'result', 'status_id', 'user_id', 'date_execution']

    def __init__(self, *args, **kwargs):
        super(task_Form, self).__init__(*args, **kwargs)
        self.fields['status_id'].queryset = status_list.objects.filter(del_status=1)
        self.fields['user_id'].queryset = UserFullName.objects.filter(is_active=1)
        # if self.instance and self.instance.pk is None:
        #     del self.fields['status_id']
        #     del self.fields['result']
        # if self.instance.user_id is not None:
        #     del self.fields['user_id']
        #     if self.instance.status_id.name == 'Назначено':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).exclude(name='Создано')
        #     elif self.instance.status_id.name == 'В работе':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).exclude(
        #             name='Создано').exclude(name='Назначено')
        #     elif self.instance.status_id.name == 'Выполнено':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).filter(name='Выполнено')
        #     elif self.instance.status_id.name == 'Выполнено с нарушением срока':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).filter(name='Выполнено с нарушением срока')

    def save(self, commit=True, user_data=None, work_data=None):
        data = super(task_Form, self).save(commit=False)
        data.user_id = user_data
        data.work_id = work_data
        if (self.instance and self.instance.pk is None) and user_data == None:
            data.status_id = status_list.objects.get(name='Создано')
        elif self.instance and self.instance.pk is None and user_data != None:
            data.status_id = status_list.objects.get(name='Назначено')
        if commit:
            data.save()
        return data


class sotr_task_Form(ModelForm):
    name = forms.CharField(label=_("Наименование"), widget=forms.TextInput(attrs={'class': 'form-control'}),
                           disabled=True)
    result = forms.CharField(label=_("Результат"), widget=forms.Textarea(attrs={'class': 'form-control'}),
                             required=False)
    status_id = forms.ModelChoiceField(label=_("Статус"), widget=forms.Select(attrs={'class': 'form-control'}),
                                       queryset=None)
    user_id = forms.ModelChoiceField(label=_("Исполнитель"), widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=None, required=False, disabled=True)
    date_execution = forms.DateField(label=_("Срок выполнения"),
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                            format=('%Y-%m-%d')), disabled=True)

    class Meta:
        model = tasks
        fields = ['name', 'user_id', 'date_execution', 'result', 'status_id']

    def __init__(self, *args, **kwargs):
        super(sotr_task_Form, self).__init__(*args, **kwargs)
        self.fields['status_id'].queryset = status_list.objects.filter(del_status=1)
        self.fields['user_id'].queryset = UserFullName.objects.filter(is_active=1)
        # if self.instance and self.instance.pk is None:
        #     del self.fields['status_id']
        #     del self.fields['result']
        # if self.instance.user_id is not None:
        #     del self.fields['user_id']
        #     if self.instance.status_id.name == 'Назначено':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).exclude(name='Создано')
        #     elif self.instance.status_id.name == 'В работе':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).exclude(
        #             name='Создано').exclude(name='Назначено')
        #     elif self.instance.status_id.name == 'Выполнено':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).filter(name='Выполнено')
        #     elif self.instance.status_id.name == 'Выполнено с нарушением срока':
        #         self.fields['status_id'].queryset = status_list.objects.filter(del_status=1).filter(name='Выполнено с нарушением срока')

    # def save(self, commit=True, user_data=None, work_data=None):
    #     data = super(task_Form, self).save(commit=False)
    #     data.user_id = user_data
    #     data.work_id = work_data
    #     if (self.instance and self.instance.pk is None) and user_data == None:
    #         data.status_id = status_list.objects.get(name='Создано')
    #     elif self.instance and self.instance.pk is None and user_data != None:
    #         data.status_id = status_list.objects.get(name='Назначено')
    #     if commit:
    #         data.save()
    #     return data
