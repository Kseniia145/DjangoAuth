from django.urls import path
from . import views

app_name = 'blogapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.all_articles, name='all_articles'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('categories/', views.categories, name='categories'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]

