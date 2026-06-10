from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from .word_utils import canonicalize_english_word


class Category(models.Model):
    name = models.CharField('Название категории', max_length=120, unique=True)
    slug = models.SlugField('Слаг', max_length=140, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or 'category'
            slug = base
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f'{base}-{counter}'
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Word(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1 — Beginner'),
        ('A2', 'A2 — Elementary'),
        ('B1', 'B1 — Intermediate'),
        ('B2', 'B2 — Upper-Intermediate'),
        ('C1', 'C1 — Advanced'),
    ]
    PART_OF_SPEECH_CHOICES = [
        ('noun', 'Существительное'),
        ('verb', 'Глагол'),
        ('adjective', 'Прилагательное'),
        ('adverb', 'Наречие'),
        ('phrase', 'Фраза'),
        ('other', 'Другое'),
    ]

    english = models.CharField('Английское слово', max_length=120, unique=True)
    translation = models.CharField('Перевод', max_length=180)
    transcription = models.CharField('Транскрипция', max_length=120, blank=True)
    example = models.TextField('Пример использования', blank=True)
    level = models.CharField('Уровень', max_length=2, choices=LEVEL_CHOICES, default='A1')
    part_of_speech = models.CharField('Часть речи', max_length=20, choices=PART_OF_SPEECH_CHOICES, default='other')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        ordering = ['english']
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'
        indexes = [
            models.Index(fields=['english']),
            models.Index(fields=['level']),
        ]

    def save(self, *args, **kwargs):
        self.english = canonicalize_english_word(self.english)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.english} — {self.translation}'


class UserWord(models.Model):
    STATUS_CHOICES = [
        ('learning', 'Изучается'),
        ('learned', 'Выучено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    word = models.ForeignKey(Word, verbose_name='Слово', on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='learning')
    correct_answers = models.PositiveIntegerField('Правильные ответы', default=0)
    wrong_answers = models.PositiveIntegerField('Ошибки', default=0)
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    last_practiced_at = models.DateTimeField('Дата последней тренировки', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'word')
        ordering = ['-added_at']
        verbose_name = 'Слово пользователя'
        verbose_name_plural = 'Слова пользователей'

    def register_answer(self, is_correct: bool):
        if is_correct:
            self.correct_answers += 1
            if self.correct_answers >= 3:
                self.status = 'learned'
        else:
            self.wrong_answers += 1
            self.status = 'learning'
        self.last_practiced_at = timezone.now()
        self.save(update_fields=['correct_answers', 'wrong_answers', 'status', 'last_practiced_at'])

    def __str__(self):
        return f'{self.user.username}: {self.word.english}'


class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    total_questions = models.PositiveIntegerField('Всего вопросов')
    correct_answers = models.PositiveIntegerField('Правильные ответы')
    created_at = models.DateTimeField('Дата прохождения', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Результат тестирования'
        verbose_name_plural = 'Результаты тестирования'

    @property
    def percent(self):
        if not self.total_questions:
            return 0
        return round(self.correct_answers / self.total_questions * 100)

    def __str__(self):
        return f'{self.user.username}: {self.correct_answers}/{self.total_questions}'


class TrainingAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    word = models.ForeignKey(Word, verbose_name='Слово', on_delete=models.CASCADE)
    answer = models.CharField('Ответ пользователя', max_length=180)
    is_correct = models.BooleanField('Верный ответ', default=False)
    created_at = models.DateTimeField('Дата ответа', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Попытка тренировки'
        verbose_name_plural = 'Попытки тренировки'

    def __str__(self):
        return f'{self.user.username}: {self.word.english} — {self.is_correct}'
