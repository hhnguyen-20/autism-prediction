# example/urls.py
from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.predict, name='predict'),
    path('result', views.result, name='result'),
]
