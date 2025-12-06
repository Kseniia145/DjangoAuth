from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Створює групи користувачів: Автор та Модератор
    з відповідними правами доступу
    """
    # Перевіряємо, чи це міграція для нашого застосунку або blogapp
    if sender.name not in ['accounts', 'blogapp', 'contenttypes']:
        return
    
    # Отримуємо ContentType для моделі Comment
    try:
        from blogapp.models import Comment
        comment_content_type = ContentType.objects.get_for_model(Comment)
    except (ContentType.DoesNotExist, ImportError):
        # Якщо ContentType ще не створений, виходимо
        return

    # Отримуємо права доступу для коментарів
    try:
        add_comment = Permission.objects.get(
            codename='add_comment',
            content_type=comment_content_type
        )
        change_comment = Permission.objects.get(
            codename='change_comment',
            content_type=comment_content_type
        )
        delete_comment = Permission.objects.get(
            codename='delete_comment',
            content_type=comment_content_type
        )
    except Permission.DoesNotExist:
        # Якщо права ще не створені, виходимо
        return

    # Створюємо або отримуємо групу "Автор"
    author_group, created = Group.objects.get_or_create(name='Автор')
    # Права для автора:
    # - додавати коментарі
    # - редагувати коментарі (власні)
    # - видаляти коментарі (власні)
    author_group.permissions.add(add_comment, change_comment, delete_comment)
    if created:
        print("Група 'Автор' створена з правами доступу")
    else:
        print("Група 'Автор' оновлена з правами доступу")

    # Створюємо або отримуємо групу "Модератор"
    moderator_group, created = Group.objects.get_or_create(name='Модератор')
    # Модератор має всі права автора
    moderator_group.permissions.add(add_comment, change_comment, delete_comment)
    if created:
        print("Група 'Модератор' створена з правами доступу")
    else:
        print("Група 'Модератор' оновлена з правами доступу")

