"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('category', views.category, name='category'),
    path('contact', views.contact, name='contact'),
    path('mail', views.mail, name='mail'),

    path('login', views.login, name='login'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('loginimpl', views.loginimpl, name='loginimpl'),
    path('register', views.register, name='register'),
    path('registerimpl', views.registerimpl, name='registerimpl'),
    path('mypage', views.mypage, name='mypage'),
    path('mypageupdate', views.mypageupdate, name='mypageupdate'),

    path('cabbage', views.Cabbage.cabbage, name='cabbage'),
    path('cabbage/analysis', views.Cabbage.analysis, name='cabbage/analysis'),

    path('pumpkin', views.Pumpkin.pumpkin, name="pumpkin"),
    path('pumpkin/analysis', views.Pumpkin.analysis, name="pumpkin/analysis"),

    path('bean', views.Bean.bean, name="bean"),
    path('bean/analysis', views.Bean.analysis, name="bean/analysis"),

    path('cucumber', views.Cucumber.cucumber, name="cucumber"),
    path('cucumber/analysis', views.Cucumber.analysis, name="cucumber/analysis"),

    path('greenonion', views.Greenonion.greenonion, name="greenonion"),
    path('greenonion/analysis', views.Greenonion.analysis, name="greenonion/analysis"),

    path('kimchi', views.Kimchi.kimchi, name="kimchi"),
    path('kimchi/analysis', views.Kimchi.analysis, name="kimchi/analysis"),

    path('pepper', views.Pepper.pepper, name="pepper"),
    path('pepper/analysis', views.Pepper.analysis, name="pepper/analysis"),

    path('radish', views.Radish.radish, name="radish"),
    path('radish/analysis', views.Radish.analysis, name="radish/analysis"),

    path('tomato', views.Tomato.tomato, name="tomato"),
    path('tomato/analysis', views.Tomato.analysis, name="tomato/analysis"),

    path('youngpumpkin', views.Youngpumpkin.youngpumpkin, name="youngpumpkin"),
    path('youngpumpkin/analysis', views.Youngpumpkin.analysis, name="youngpumpkin/analysis"),


]
