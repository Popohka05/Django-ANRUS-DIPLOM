from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from vocabulary.demo_words import DEMO_CATEGORIES, DEMO_WORDS
from vocabulary.models import Category, UserWord, Word


class Command(BaseCommand):
    help = 'Загружает демонстрационные слова по уровням и учебного пользователя.'

    def handle(self, *args, **options):
        demo_user, created = User.objects.get_or_create(username='demo_student', defaults={'email': 'demo@example.com'})
        demo_user.set_password('DemoPass2026!')
        demo_user.save()

        categories = {
            category_name: Category.objects.get_or_create(name=category_name)[0]
            for category_name in DEMO_CATEGORIES
        }

        for english, translation, transcription, example, level, part_of_speech, category_name in DEMO_WORDS:
            word, _ = Word.objects.update_or_create(
                english=english,
                defaults={
                    'translation': translation,
                    'transcription': transcription,
                    'example': example,
                    'level': level,
                    'part_of_speech': part_of_speech,
                    'category': categories[category_name],
                    'created_by': demo_user,
                },
            )
            UserWord.objects.get_or_create(user=demo_user, word=word)

        self.stdout.write(self.style.SUCCESS('Demo data loaded. Login: demo_student / DemoPass2026!'))
