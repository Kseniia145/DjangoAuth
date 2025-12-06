from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True, help_text='Ім\'я автора (для анонімних авторів)')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', help_text='Користувач-автор статті')
    text = models.TextField()
    image = models.CharField(max_length=255)
    publication_date = models.DateField()
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    
    def get_author_name(self):
        """Повертає ім'я автора: або username користувача, або поле author"""
        if self.user:
            return self.user.username
        return self.author or 'Анонімний автор'


class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True, help_text='Ім\'я автора (для анонімних авторів)')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='comments', help_text='Користувач-автор коментаря')
    publication_date = models.DateField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        author_name = self.get_author_name()
        return f"{author_name}: {self.text[:50]}"
    
    def get_author_name(self):
        """Повертає ім'я автора: або username користувача, або поле author"""
        if self.user:
            return self.user.username
        return self.author or 'Анонімний автор'
    
    def can_edit(self, user):
        """Перевіряє, чи може користувач редагувати коментар"""
        if not user.is_authenticated:
            return False
        # Автор може редагувати тільки свої коментарі
        if self.user == user:
            return True
        return False
    
    def can_delete(self, user):
        """Перевіряє, чи може користувач видаляти коментар"""
        if not user.is_authenticated:
            return False
        # Автор може видаляти тільки свої коментарі
        if self.user == user:
            return True
        # Модератор може видаляти будь-які коментарі
        if user.groups.filter(name='Модератор').exists():
            return True
        return False
