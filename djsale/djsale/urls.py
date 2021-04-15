from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from app_sitemap.sitemap import NewsSitemap, StaticPagesSitemap, HousingSitemap


sitemaps = {
    'news': NewsSitemap,
    'static': StaticPagesSitemap,
    'housing': HousingSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_info.urls')),
    path('news/', include('app_news.urls')),
    path('rss/', include('app_rss.urls')),
    path('housing/', include('app_property.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]






