from django.urls import path

from . import views


urlpatterns = [
    path('news_list', views.NewsListView.as_view(), name='news_list'),  # страница списка новостей
    path('detail/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),  # страница новости
]
