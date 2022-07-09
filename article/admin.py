from django.contrib import admin

# Register your models here.
from article.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", 'author', "created_at", "updated_at", "title", "image", "author_email")

    def author_email(self, obj):
        return obj.author.email


admin.site.register(Article, ArticleAdmin)
