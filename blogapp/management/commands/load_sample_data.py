from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from blogapp.models import Category, Tag, Article, Comment
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Завантажує прикладні дані в базу даних'

    def handle(self, *args, **options):
        self.stdout.write('Початок завантаження прикладних даних...')
        
        # Створюємо користувачів
        self.stdout.write('Створення користувачів...')
        users = []
        
        # Створюємо кілька користувачів
        user_data = [
            {'username': 'ivan_petrov', 'email': 'ivan@example.com', 'password': 'password123'},
            {'username': 'maria_koval', 'email': 'maria@example.com', 'password': 'password123'},
            {'username': 'oleg_sidorov', 'email': 'oleg@example.com', 'password': 'password123'},
            {'username': 'anna_ivanova', 'email': 'anna@example.com', 'password': 'password123'},
        ]
        
        for user_info in user_data:
            user, created = User.objects.get_or_create(
                username=user_info['username'],
                defaults={'email': user_info['email']}
            )
            if created:
                user.set_password(user_info['password'])
                user.save()
                # Додаємо до групи "Автор"
                try:
                    author_group = Group.objects.get(name='Автор')
                    user.groups.add(author_group)
                except Group.DoesNotExist:
                    pass
            users.append(user)
            self.stdout.write(f'  ✓ Користувач {user.username} створено')
        
        # Створюємо модератора
        moderator, created = User.objects.get_or_create(
            username='moderator',
            defaults={'email': 'moderator@example.com'}
        )
        if created:
            moderator.set_password('moderator123')
            moderator.save()
            try:
                moderator_group = Group.objects.get(name='Модератор')
                moderator.groups.add(moderator_group)
            except Group.DoesNotExist:
                pass
            self.stdout.write(f'  ✓ Модератор {moderator.username} створено')
        
        # Створюємо категорії
        self.stdout.write('Створення категорій...')
        categories_data = [
            {'title': 'Технології', 'description': 'Статті про технології та програмування', 'icon': 'fas fa-laptop-code'},
            {'title': 'Наука', 'description': 'Наукові дослідження та відкриття', 'icon': 'fas fa-flask'},
            {'title': 'Культура', 'description': 'Культурні події та мистецтво', 'icon': 'fas fa-palette'},
            {'title': 'Спорт', 'description': 'Спортивні новини та події', 'icon': 'fas fa-futbol'},
            {'title': 'Подорожі', 'description': 'Цікаві місця та подорожі', 'icon': 'fas fa-plane'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                title=cat_data['title'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'  ✓ Категорія {category.title} створено')
        
        # Створюємо теги
        self.stdout.write('Створення тегів...')
        tags_data = [
            'Python', 'Django', 'JavaScript', 'React', 'Веб-розробка',
            'Штучний інтелект', 'Машинне навчання', 'Кібербезпека',
            'Фотографія', 'Музика', 'Література', 'Кіно',
            'Футбол', 'Баскетбол', 'Теніс', 'Плавання',
            'Європа', 'Азія', 'Америка', 'Африка'
        ]
        
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(title=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'  ✓ Тег {tag.title} створено')
        
        # Створюємо статті
        self.stdout.write('Створення статей...')
        articles_data = [
            {
                'title': 'Вступ до Django: Створення веб-додатків на Python',
                'text': '''Django - це потужний веб-фреймворк для Python, який дозволяє швидко створювати складні веб-додатки. 
                У цій статті ми розглянемо основи Django, його архітектуру та основні концепції.
                
                Django надає багато корисних інструментів для розробки: ORM для роботи з базою даних, систему шаблонів,
                автоматичну адміністративну панель та багато іншого. Це робить його ідеальним вибором для швидкої розробки.
                
                Почнемо з встановлення Django та створення першого проєкту. Після цього ми створимо простий додаток
                та розглянемо основні компоненти Django.''',
                'image': 'https://via.placeholder.com/800x400?text=Django',
                'author': None,
                'user': users[0] if users else None,
                'category': categories[0],
                'tags': ['Python', 'Django', 'Веб-розробка'],
                'days_ago': 5
            },
            {
                'title': 'Штучний інтелект у сучасному світі',
                'text': '''Штучний інтелект (AI) стає все більш важливою частиною нашого життя. Від голосових помічників
                до автономних автомобілів, AI трансформує різні галузі.
                
                У цій статті ми розглянемо поточний стан технологій штучного інтелекту, їх застосування та майбутні перспективи.
                Також обговоримо етичні питання, пов'язані з розвитком AI.
                
                Машинне навчання є однією з ключових технологій AI. Воно дозволяє комп'ютерам навчатися на даних
                та робити прогнози без явного програмування.''',
                'image': 'https://via.placeholder.com/800x400?text=AI',
                'author': None,
                'user': users[1] if len(users) > 1 else None,
                'category': categories[1],
                'tags': ['Штучний інтелект', 'Машинне навчання'],
                'days_ago': 3
            },
            {
                'title': 'Найкращі місця для подорожей у Європі',
                'text': '''Європа багата на чудові місця для подорожей. Від історичних міст до мальовничих природних ландшафтів,
                тут є щось для кожного мандрівника.
                
                У цій статті ми розглянемо топ-10 місць, які обов'язково варто відвідати в Європі. Це включає
                Париж з його Ейфелевою вежею, Рим з його античною історією, та багато інших чудових місць.
                
                Кожне місце має свою унікальну атмосферу та культуру. Відправляючись у подорож, ви отримаєте
                незабутні враження та збагатите свій досвід.''',
                'image': 'https://via.placeholder.com/800x400?text=Travel',
                'author': 'Анонімний мандрівник',
                'user': None,
                'category': categories[4],
                'tags': ['Європа', 'Подорожі'],
                'days_ago': 7
            },
            {
                'title': 'Футбол: Історія та розвиток гри',
                'text': '''Футбол - це найпопулярніший вид спорту у світі. Мільйони людей грають та спостерігають за цією грою
                по всьому світу.
                
                У цій статті ми розглянемо історію футболу від його витоків до сучасного стану. Також обговоримо
                правила гри, найвідоміші турніри та легендарних гравців.
                
                Футбол об'єднує людей з різних країн та культур. Це більше ніж просто гра - це спосіб життя
                для мільйонів вболівальників по всьому світу.''',
                'image': 'https://via.placeholder.com/800x400?text=Football',
                'author': None,
                'user': users[2] if len(users) > 2 else None,
                'category': categories[3],
                'tags': ['Футбол', 'Спорт'],
                'days_ago': 2
            },
            {
                'title': 'Сучасне мистецтво та його вплив на суспільство',
                'text': '''Сучасне мистецтво відображає дух часу та впливає на суспільство різними способами.
                Від живопису до цифрового мистецтва, мистецтво постійно еволюціонує.
                
                У цій статті ми розглянемо різні напрямки сучасного мистецтва, його вплив на культуру
                та те, як воно відображає сучасні проблеми та тенденції.
                
                Мистецтво має силу змінювати світогляд людей та надихати на зміни. Воно є важливою
                частиною культурної спадщини людства.''',
                'image': 'https://via.placeholder.com/800x400?text=Art',
                'author': None,
                'user': users[3] if len(users) > 3 else None,
                'category': categories[2],
                'tags': ['Культура', 'Мистецтво'],
                'days_ago': 1
            },
        ]
        
        articles = []
        for art_data in articles_data:
            article, created = Article.objects.get_or_create(
                title=art_data['title'],
                defaults={
                    'text': art_data['text'],
                    'image': art_data['image'],
                    'author': art_data['author'],
                    'user': art_data['user'],
                    'category': art_data['category'],
                    'publication_date': date.today() - timedelta(days=art_data['days_ago']),
                    'is_published': True
                }
            )
            if created:
                # Додаємо теги
                for tag_name in art_data['tags']:
                    tag = next((t for t in tags if t.title == tag_name), None)
                    if tag:
                        article.tag.add(tag)
                articles.append(article)
                self.stdout.write(f'  ✓ Стаття "{article.title}" створено')
        
        # Створюємо коментарі
        self.stdout.write('Створення коментарів...')
        comments_data = [
            {'text': 'Дуже цікава стаття! Дякую за корисну інформацію про Django.', 'user': users[1] if len(users) > 1 else None, 'author': None, 'article_idx': 0},
            {'text': 'Чудово написано! Як раз вивчаю Django і це дуже допомогло.', 'user': users[2] if len(users) > 2 else None, 'author': None, 'article_idx': 0},
            {'text': 'AI - це майбутнє! Цікаво, що буде далі.', 'user': None, 'author': 'Гість', 'article_idx': 1},
            {'text': 'Повністю згоден з автором. Штучний інтелект змінює світ.', 'user': users[0] if users else None, 'author': None, 'article_idx': 1},
            {'text': 'Був у Парижі минулого року - незабутні враження!', 'user': users[3] if len(users) > 3 else None, 'author': None, 'article_idx': 2},
            {'text': 'Дякую за підбірку! Обов\'язково відвідаю ці місця.', 'user': None, 'author': 'Мандрівник', 'article_idx': 2},
            {'text': 'Футбол - це життя! Найкращий вид спорту.', 'user': users[1] if len(users) > 1 else None, 'author': None, 'article_idx': 3},
            {'text': 'Цікава стаття про мистецтво. Дякую!', 'user': None, 'author': 'Любитель мистецтва', 'article_idx': 4},
        ]
        
        for comment_data in comments_data:
            if comment_data['article_idx'] < len(articles):
                article = articles[comment_data['article_idx']]
                comment = Comment.objects.create(
                    text=comment_data['text'],
                    author=comment_data['author'],
                    user=comment_data['user'],
                    article=article,
                    publication_date=date.today() - timedelta(days=random.randint(0, comment_data['article_idx']))
                )
                self.stdout.write(f'  ✓ Коментар до статті "{article.title}" створено')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Всі прикладні дані успішно завантажено!'))
        self.stdout.write(f'\nСтворено:')
        self.stdout.write(f'  - Користувачів: {User.objects.count()}')
        self.stdout.write(f'  - Категорій: {Category.objects.count()}')
        self.stdout.write(f'  - Тегів: {Tag.objects.count()}')
        self.stdout.write(f'  - Статей: {Article.objects.filter(is_published=True).count()}')
        self.stdout.write(f'  - Коментарів: {Comment.objects.count()}')
        self.stdout.write(f'\nТестові облікові дані:')
        self.stdout.write(f'  - Користувач: ivan_petrov / password123')
        self.stdout.write(f'  - Користувач: maria_koval / password123')
        self.stdout.write(f'  - Модератор: moderator / moderator123')

