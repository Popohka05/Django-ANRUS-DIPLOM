from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Word
from .word_utils import canonicalize_english_word


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ('english', 'translation', 'transcription', 'example', 'level', 'part_of_speech')
        widgets = {
            'english': forms.TextInput(attrs={'placeholder': 'Например: achievement или achievements'}),
            'translation': forms.TextInput(attrs={'placeholder': 'Например: достижение'}),
            'transcription': forms.TextInput(attrs={'placeholder': '[əˈtʃiːvmənt]'}),
            'example': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Пример предложения на английском'}),
        }
        help_texts = {
            'english': 'Если введено множественное число, система сохранит каноническую форму.',
        }

    def clean_english(self):
        canonical = canonicalize_english_word(self.cleaned_data['english'])
        duplicate = Word.objects.filter(english=canonical)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise forms.ValidationError(f'Слово уже есть в базе в канонической форме: {canonical}')
        return canonical


class TrainingAnswerForm(forms.Form):
    answer = forms.CharField(label='Ваш перевод', max_length=180, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
