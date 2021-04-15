from django.urls import path

from .feed import NewsFeed


urlpatterns = [
    path('news/feed', NewsFeed(), name='news_rss'),  # лента новостей
]
