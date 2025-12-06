from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.publication_date = date.today()
            comment.save()
            messages.success(request, 'Ваш коментар успішно додано!')
            return redirect('blogapp:article_detail', article_id=article.id)
    else:
        form = CommentForm()
    
    return render(request, 'blogapp/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })


def categories(request):
    categories_list = Category.objects.all()
    return render(request, 'blogapp/categories.html', {'categories': categories_list})
