import random
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm, TrainingAnswerForm, WordForm
from .models import Category, QuizResult, TrainingAttempt, UserWord, Word


def normalize_answer(value: str) -> str:
    return value.strip().lower().replace('ё', 'е')


def home(request):
    return render(request, 'vocabulary/home.html', {
        'words_count': Word.objects.count(),
        'categories_count': Category.objects.count(),
        'users_count': User.objects.count(),
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Аккаунт создан. Можно начать обучение.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'vocabulary/register.html', {'form': form})


@login_required
def dashboard(request):
    user_words = UserWord.objects.filter(user=request.user)
    results = QuizResult.objects.filter(user=request.user)[:5]
    attempts = TrainingAttempt.objects.filter(user=request.user)[:5]
    return render(request, 'vocabulary/dashboard.html', {
        'learning_count': user_words.filter(status='learning').count(),
        'learned_count': user_words.filter(status='learned').count(),
        'correct_total': sum(item.correct_answers for item in user_words),
        'wrong_total': sum(item.wrong_answers for item in user_words),
        'results': results,
        'attempts': attempts,
    })


def word_list(request):
    query = request.GET.get('q', '').strip()
    level = request.GET.get('level', '').strip()
    category_slug = request.GET.get('category', '').strip()
    words = Word.objects.select_related('category').all()
    if query:
        words = words.filter(Q(english__icontains=query) | Q(translation__icontains=query) | Q(example__icontains=query))
    if level:
        words = words.filter(level=level)
    if category_slug:
        words = words.filter(category__slug=category_slug)
    return render(request, 'vocabulary/word_list.html', {
        'words': words,
        'query': query,
        'level': level,
        'category_slug': category_slug,
        'levels': Word.LEVEL_CHOICES,
        'categories': Category.objects.all(),
    })


def word_detail(request, pk):
    word = get_object_or_404(Word.objects.select_related('category'), pk=pk)
    user_word = None
    if request.user.is_authenticated:
        user_word = UserWord.objects.filter(user=request.user, word=word).first()
    return render(request, 'vocabulary/word_detail.html', {'word': word, 'user_word': user_word})


@login_required
def word_create(request):
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.created_by = request.user
            word.save()
            form.save_m2m()
            messages.success(request, 'Слово добавлено в общий словарь.')
            return redirect('word_detail', pk=word.pk)
    else:
        form = WordForm()
    return render(request, 'vocabulary/word_form.html', {'form': form, 'title': 'Добавить слово'})


@login_required
def word_edit(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if word.created_by != request.user and not request.user.is_staff:
        messages.error(request, 'Редактировать можно только свои слова.')
        return redirect('word_detail', pk=word.pk)
    if request.method == 'POST':
        form = WordForm(request.POST, instance=word)
        if form.is_valid():
            form.save()
            messages.success(request, 'Слово обновлено.')
            return redirect('word_detail', pk=word.pk)
    else:
        form = WordForm(instance=word)
    return render(request, 'vocabulary/word_form.html', {'form': form, 'title': 'Редактировать слово'})


@login_required
def add_to_dictionary(request, pk):
    word = get_object_or_404(Word, pk=pk)
    UserWord.objects.get_or_create(user=request.user, word=word)
    messages.success(request, 'Слово добавлено в личный словарь.')
    return redirect('word_detail', pk=word.pk)


@login_required
def my_words(request):
    status = request.GET.get('status', '')
    user_words = UserWord.objects.select_related('word', 'word__category').filter(user=request.user)
    if status in {'learning', 'learned'}:
        user_words = user_words.filter(status=status)
    return render(request, 'vocabulary/my_words.html', {'user_words': user_words, 'status': status})


@login_required
def mark_learned(request, pk):
    item = get_object_or_404(UserWord, pk=pk, user=request.user)
    item.status = 'learned'
    item.save(update_fields=['status'])
    messages.success(request, 'Слово отмечено как выученное.')
    return redirect('my_words')


@login_required
def mark_learning(request, pk):
    item = get_object_or_404(UserWord, pk=pk, user=request.user)
    item.status = 'learning'
    item.save(update_fields=['status'])
    messages.success(request, 'Слово возвращено в изучение.')
    return redirect('my_words')


@login_required
def remove_from_dictionary(request, pk):
    item = get_object_or_404(UserWord, pk=pk, user=request.user)
    item.delete()
    messages.success(request, 'Слово удалено из личного словаря.')
    return redirect('my_words')


@login_required
def training(request):
    current = UserWord.objects.select_related('word').filter(user=request.user, status='learning').order_by('last_practiced_at', 'added_at').first()
    form = TrainingAnswerForm(request.POST or None)
    result = None
    if request.method == 'POST' and current and form.is_valid():
        answer = form.cleaned_data['answer']
        is_correct = normalize_answer(answer) == normalize_answer(current.word.translation)
        TrainingAttempt.objects.create(user=request.user, word=current.word, answer=answer, is_correct=is_correct)
        current.register_answer(is_correct)
        result = {
            'is_correct': is_correct,
            'expected': current.word.translation,
            'word': current.word.english,
        }
        form = TrainingAnswerForm()
    return render(request, 'vocabulary/training.html', {'current': current, 'form': form, 'result': result})


@login_required
def quiz(request):
    words = list(Word.objects.all())
    questions = []
    result = None
    if request.method == 'POST':
        total = int(request.POST.get('total', '0') or 0)
        correct = 0
        for key, value in request.POST.items():
            if not key.startswith('word_'):
                continue
            word_id = int(key.replace('word_', ''))
            word = get_object_or_404(Word, id=word_id)
            if normalize_answer(value) == normalize_answer(word.translation):
                correct += 1
                user_word, _ = UserWord.objects.get_or_create(user=request.user, word=word)
                user_word.register_answer(True)
        result = QuizResult.objects.create(user=request.user, total_questions=total, correct_answers=correct)
    elif words:
        selected = random.sample(words, min(5, len(words)))
        translations = [word.translation for word in words]
        for word in selected:
            wrong = [value for value in translations if value != word.translation]
            options = random.sample(wrong, min(3, len(wrong))) + [word.translation]
            random.shuffle(options)
            questions.append({'word': word, 'options': options})
    return render(request, 'vocabulary/quiz.html', {'questions': questions, 'result': result})
