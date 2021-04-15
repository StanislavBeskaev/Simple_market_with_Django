from django.urls import path, include

from . import views

urlpatterns = [
    path('contacts', views.contact_view, name='contacts'),  # страница контактов
    path('about', views.about_view, name='about'),  # страница О нас
    path('main', views.main_view, name='main'),  # главная страница
]
