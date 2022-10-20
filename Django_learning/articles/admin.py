from django.contrib import admin

# Register your models here.
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'short_content']
    list_display_links = ['title']
    search_fields = ['title']

    def short_content(self, obj):
        return obj.content[:15]+"..." if len(obj.content) > 15 else obj.content


admin.site.register(Article, ArticleAdmin)
