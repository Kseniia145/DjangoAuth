from django.contrib import admin
from .models import Category, Tag, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon')
    search_fields = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publication_date', 'is_published')
    list_filter = ('is_published', 'category', 'publication_date')
    search_fields = ('title', 'author', 'text')
    filter_horizontal = ('tag',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('author', 'text')
