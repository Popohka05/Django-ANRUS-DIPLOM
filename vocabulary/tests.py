from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .forms import WordForm
from .models import Category, QuizResult, UserWord, Word
from .word_utils import canonicalize_english_word


class VocabularyFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student', password='StrongPass123!')
        category = Category.objects.create(name='Education')
        self.word = Word.objects.create(
            english='knowledge',
            translation='знание',
            transcription='[ˈnɒlɪdʒ]',
            example='Knowledge grows with practice.',
            level='A2',
            category=category,
        )
        Word.objects.create(english='goal', translation='цель', level='A1', category=category)
        Word.objects.create(english='skill', translation='навык', level='A2', category=category)
        Word.objects.create(english='progress', translation='прогресс', level='B1', category=category)

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'АНРУС')

    def test_dictionary_search(self):
        response = self.client.get(reverse('word_list'), {'q': 'knowledge'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'knowledge')

    def test_dictionary_search_uses_canonical_word_form(self):
        Word.objects.create(english='book', translation='книга', level='A1')
        response = self.client.get(reverse('word_list'), {'q': 'books'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'book')

    def test_add_word_to_personal_dictionary(self):
        self.client.login(username='student', password='StrongPass123!')
        response = self.client.get(reverse('add_to_dictionary', args=[self.word.pk]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserWord.objects.filter(user=self.user, word=self.word).exists())

    def test_training_records_correct_answer(self):
        self.client.login(username='student', password='StrongPass123!')
        UserWord.objects.create(user=self.user, word=self.word)
        response = self.client.post(reverse('training'), {'answer': 'знание'}, follow=True)
        self.assertEqual(response.status_code, 200)
        item = UserWord.objects.get(user=self.user, word=self.word)
        self.assertEqual(item.correct_answers, 1)

    def test_quiz_creates_result(self):
        self.client.login(username='student', password='StrongPass123!')
        response = self.client.post(reverse('quiz'), {f'word_{self.word.pk}': 'знание', 'total': '1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(QuizResult.objects.filter(user=self.user).count(), 1)

    def test_word_is_saved_in_canonical_form(self):
        word = Word.objects.create(english='Books', translation='книга', level='A1')
        self.assertEqual(word.english, 'book')
        self.assertEqual(canonicalize_english_word('studies'), 'study')
        self.assertEqual(canonicalize_english_word('analysis'), 'analysis')
        self.assertEqual(canonicalize_english_word('business'), 'business')

    def test_word_form_rejects_duplicate_plural_form(self):
        Word.objects.create(english='book', translation='книга', level='A1')
        form = WordForm(data={
            'english': 'books',
            'translation': 'книги',
            'level': 'A1',
            'part_of_speech': 'noun',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('book', form.errors['english'][0])
