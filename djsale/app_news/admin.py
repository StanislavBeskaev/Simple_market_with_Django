from django.contrib import admin

from .models import News


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'created_date']

