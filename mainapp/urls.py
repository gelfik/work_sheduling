"""MIPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='main_url'),
    re_path(r'worklist/([0-9]+)/tasklist([0-9]+)/', views.tasklist_update_view, name='tasklist_update_url'),
    re_path(r'worklist/([0-9]+)/tasklist', views.tasklist_view, name='tasklist_url'),
    re_path(r'worklist/([0-9]+)/', views.worklist_update_view, name='worklist_update_url'),
    path('worklist/', views.worklist_view, name='worklist_url'),
    path('userlist/', views.userlist_view, name='userlist_url'),

    path('tasklist/', views.sotr_tasklist_view, name='sotr_tasklist_url'),

    path('profile/', views.profile_view, name='profile_url'),
    path('auth/', include('authapp.urls')),
]
