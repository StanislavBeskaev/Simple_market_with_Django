from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.feedgenerator import DefaultFeed

from app_news.models import News


class CorrectMimeTypeFeed(DefaultFeed):
    content_type = 'application/xml; charset=utf-8'


class NewsFeed(Feed):
    title = "Новости"
    link = "/news/news_list"
    description = "Самые свежие новости"
    feed_type = CorrectMimeTypeFeed

    def items(self) -> QuerySet:
        return News.objects.order_by('-created_date').all()[:5]

    def item_title(self, item: News) -> str:
        return item.title

    def item_description(self, item: News) -> str:
        return item.text

    def item_link(self, item: News) -> str:
        return reverse('news_detail', args=[str(item.pk)])
