from django.apps import AppConfig
import os


class BlogappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blogapp"

    def ready(self):
        """Створює суперкористувача за замовчуванням, якщо його не існує"""
        # Перевіряємо, чи не запущено через migrate або інші команди
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        try:
            from django.contrib.auth.models import User
            # Створюємо суперкористувача, якщо його немає
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin'
                )
        except Exception:
            # Ігноруємо помилки під час імпорту моделей або підключення до БД
            pass
