from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Article, Category, Comment
from .forms import CommentForm
from datetime import date


def index(request):
    articles = Article.objects.filter(is_published=True).order_by('-publication_date')[:3]
    return render(request, 'blogapp/index.html', {'articles': articles})


def all_articles(request):
    articles = Article.objects.filter(is_published=True).order_by('-publication_date')
    return render(request, 'blogapp/all_articles.html', {'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, is_published=True)
    comments = Comment.objects.filter(article=article).order_by('-publication_date')
    
    # Додаємо інформацію про права доступу для кожного коментаря
    comments_with_permissions = []
    for comment in comments:
        comments_with_permissions.append({
            'comment': comment,
            'can_edit': comment.can_edit(request.user) if request.user.is_authenticated else False,
            'can_delete': comment.can_delete(request.user) if request.user.is_authenticated else False,
        })
    
    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.publication_date = date.today()
            # Якщо користувач авторизований, встановлюємо user
            if request.user.is_authenticated:
                comment.user = request.user
                # Якщо поле author порожнє, очищаємо його
                if not comment.author:
                    comment.author = None
            # Якщо користувач не авторизований, перевіряємо, чи заповнене поле author
            elif not comment.author:
                form.add_error('author', 'Введіть ваше ім\'я або увійдіть в систему')
                return render(request, 'blogapp/article_detail.html', {
                    'article': article,
                    'comments_with_permissions': comments_with_permissions,
                    'form': form
                })
            comment.save()
            messages.success(request, 'Ваш коментар успішно додано!')
            return redirect('blogapp:article_detail', article_id=article.id)
    else:
        form = CommentForm(user=request.user)
    
    return render(request, 'blogapp/article_detail.html', {
        'article': article,
        'comments_with_permissions': comments_with_permissions,
        'form': form
    })


def categories(request):
    categories_list = Category.objects.all()
    return render(request, 'blogapp/categories.html', {'categories': categories_list})


@login_required
def edit_comment(request, comment_id):
    """Редагування коментаря"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Перевіряємо права доступу
    if not comment.can_edit(request.user):
        messages.error(request, 'У вас немає прав для редагування цього коментаря.')
        return redirect('blogapp:article_detail', article_id=comment.article.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment, user=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            # При редагуванні завжди зберігаємо user (якщо користувач авторизований)
            if request.user.is_authenticated:
                comment.user = request.user
                if not comment.author:
                    comment.author = None
            comment.save()
            messages.success(request, 'Коментар успішно оновлено!')
            return redirect('blogapp:article_detail', article_id=comment.article.id)
    else:
        form = CommentForm(instance=comment, user=request.user)
    
    return render(request, 'blogapp/edit_comment.html', {
        'form': form,
        'comment': comment,
        'article': comment.article
    })


@login_required
def delete_comment(request, comment_id):
    """Видалення коментаря"""
    comment = get_object_or_404(Comment, id=comment_id)
    article_id = comment.article.id
    
    # Перевіряємо права доступу
    if not comment.can_delete(request.user):
        messages.error(request, 'У вас немає прав для видалення цього коментаря.')
        return redirect('blogapp:article_detail', article_id=article_id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Коментар успішно видалено!')
        return redirect('blogapp:article_detail', article_id=article_id)
    
    return render(request, 'blogapp/delete_comment.html', {
        'comment': comment,
        'article': comment.article
    })
