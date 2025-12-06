from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import UserRegisterForm, UserLoginForm


def register(request):
    """Реєстрація нового користувача"""
    if request.user.is_authenticated:
        messages.info(request, 'Ви вже авторизовані!')
        return redirect('blogapp:index')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Додаємо користувача до групи "Автор"
            try:
                author_group = Group.objects.get(name='Автор')
                user.groups.add(author_group)
            except Group.DoesNotExist:
                pass
            
            messages.success(request, f'Акаунт {user.username} успішно створено! Ви тепер авторизовані як Автор.')
            login(request, user)
            return redirect('blogapp:index')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """Вхід користувача в систему"""
    if request.user.is_authenticated:
        messages.info(request, 'Ви вже авторизовані!')
        return redirect('blogapp:index')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Вітаємо, {user.username}! Ви успішно увійшли в систему.')
            # Перенаправляємо на сторінку, з якої прийшов користувач, або на головну
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            return redirect('blogapp:index')
        else:
            messages.error(request, 'Невірне ім\'я користувача або пароль.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """Вихід користувача з системи"""
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'Ви успішно вийшли з системи. До побачення, {username}!')
    else:
        messages.info(request, 'Ви не авторизовані.')
    
    return redirect('blogapp:index')
