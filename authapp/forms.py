from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError


class UserAddForm(UserCreationForm):
    username = forms.CharField(label=_("Логин"),
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(label=_("Email"),
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                             max_length=64)
    last_name = forms.CharField(label=_("Фамилия"),
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
                                max_length=32)
    first_name = forms.CharField(label=_("Имя"),
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
                                 max_length=32)
    password1 = forms.CharField(label=_("Пароль"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label=_("Подтверждение пароля"), widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}))
    group_data = forms.ModelChoiceField(label=_("Должность"), widget=forms.Select(attrs={'class': 'form-control'}),
                                            queryset=None)

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True, password="unknown", username="unknown"):
        self.cleaned_data["password1"] = password
        user = super(UserAddForm, self).save(commit=False)
        user.set_password(password)
        user.username = username
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        self.fields['group_data'].queryset = Group.objects.all()
        del self.fields['username']
        del self.fields['password1']
        del self.fields['password2']
