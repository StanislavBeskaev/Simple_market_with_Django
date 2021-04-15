from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from app_news.models import News
from app_property.models import Housing


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return News.objects.all()


class StaticPagesSitemap(Sitemap):
    priority = 0.5
    changefreq = 'never'

    def items(self):
        return ['about', 'contacts']

    def location(self, item):
        return reverse(item)


class HousingSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Housing.objects.all()
