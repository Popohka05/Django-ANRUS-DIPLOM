from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from vocabulary.models import Category, UserWord, Word


class Command(BaseCommand):
    help = 'Загружает демонстрационные категории, слова и учебного пользователя.'

    def handle(self, *args, **options):
        demo_user, created = User.objects.get_or_create(username='demo_student', defaults={'email': 'demo@example.com'})
        demo_user.set_password('DemoPass2026!')
        demo_user.save()

        data = {
            'Education': [
                ('knowledge', 'знание', '[ˈnɒlɪdʒ]', 'Knowledge grows with practice.', 'A2', 'noun'),
                ('skill', 'навык', '[skɪl]', 'This course improves your speaking skill.', 'A2', 'noun'),
                ('achievement', 'достижение', '[əˈtʃiːvmənt]', 'Passing the exam was a great achievement.', 'B1', 'noun'),
                ('assignment', 'задание', '[əˈsaɪnmənt]', 'The teacher gave us a new assignment.', 'B1', 'noun'),
            ],
            'Daily life': [
                ('journey', 'путешествие', '[ˈdʒɜːni]', 'The journey took three hours.', 'A2', 'noun'),
                ('habit', 'привычка', '[ˈhæbɪt]', 'Reading every day is a useful habit.', 'A2', 'noun'),
                ('schedule', 'расписание', '[ˈʃedjuːl]', 'I checked my schedule for tomorrow.', 'B1', 'noun'),
                ('choice', 'выбор', '[tʃɔɪs]', 'You have a choice between two options.', 'A2', 'noun'),
            ],
            'Work': [
                ('deadline', 'срок сдачи', '[ˈdedlaɪn]', 'The project deadline is next week.', 'B1', 'noun'),
                ('improve', 'улучшать', '[ɪmˈpruːv]', 'Practice helps improve vocabulary.', 'A2', 'verb'),
                ('review', 'проверять', '[rɪˈvjuː]', 'Please review the report before sending it.', 'B1', 'verb'),
                ('requirement', 'требование', '[rɪˈkwaɪəmənt]', 'The application meets the main requirement.', 'B2', 'noun'),
            ],
        }

        for category_name, words in data.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            for english, translation, transcription, example, level, part_of_speech in words:
                word, _ = Word.objects.update_or_create(
                    english=english,
                    defaults={
                        'translation': translation,
                        'transcription': transcription,
                        'example': example,
                        'level': level,
                        'part_of_speech': part_of_speech,
                        'category': category,
                        'created_by': demo_user,
                    },
                )
                UserWord.objects.get_or_create(user=demo_user, word=word)

        self.stdout.write(self.style.SUCCESS('Demo data loaded. Login: demo_student / DemoPass2026!'))
