from django.views import generic

from .models import News


class NewsListView(generic.ListView):
    model = News
    queryset = News.objects.order_by('-created_date').all()
    template_name = 'app_news/news_list.html'
    context_object_name = 'news_list'


class NewsDetailView(generic.DetailView):
    model = News
    queryset = News.objects.all()
    template_name = 'app_news/news_detail.html'
    context_object_name = 'news'
