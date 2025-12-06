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
    list_display = ('title', 'get_author_name', 'user', 'category', 'publication_date', 'is_published')
    list_filter = ('is_published', 'category', 'publication_date', 'user')
    search_fields = ('title', 'author', 'text', 'user__username')
    filter_horizontal = ('tag',)
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'text', 'image', 'category', 'tag')
        }),
        ('Автор', {
            'fields': ('user', 'author'),
            'description': 'Вкажіть користувача або ім\'я автора для анонімних статей'
        }),
        ('Публікація', {
            'fields': ('publication_date', 'is_published')
        }),
    )
    
    def get_author_name(self, obj):
        return obj.get_author_name()
    get_author_name.short_description = 'Автор'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_author_name', 'user', 'article', 'publication_date')
    list_filter = ('publication_date', 'user')
    search_fields = ('author', 'text', 'user__username')
    fieldsets = (
        ('Коментар', {
            'fields': ('article', 'text', 'publication_date')
        }),
        ('Автор', {
            'fields': ('user', 'author'),
            'description': 'Вкажіть користувача або ім\'я автора для анонімних коментарів'
        }),
    )
    
    def get_author_name(self, obj):
        return obj.get_author_name()
    get_author_name.short_description = 'Автор'
