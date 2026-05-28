from django.contrib import admin
from .models import Category, QuizResult, TrainingAttempt, UserWord, Word


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('english', 'translation', 'level', 'part_of_speech', 'category', 'created_at')
    list_filter = ('level', 'part_of_speech', 'category')
    search_fields = ('english', 'translation', 'example')
    autocomplete_fields = ('category', 'created_by')


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'status', 'correct_answers', 'wrong_answers', 'last_practiced_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'word__english', 'word__translation')


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'correct_answers', 'total_questions', 'percent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)


@admin.register(TrainingAttempt)
class TrainingAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'answer', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('user__username', 'word__english', 'answer')
