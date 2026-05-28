from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Word


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ('english', 'translation', 'transcription', 'example', 'level', 'part_of_speech', 'category')
        widgets = {
            'english': forms.TextInput(attrs={'placeholder': 'Например: achievement'}),
            'translation': forms.TextInput(attrs={'placeholder': 'Например: достижение'}),
            'transcription': forms.TextInput(attrs={'placeholder': '[əˈtʃiːvmənt]'}),
            'example': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Пример предложения на английском'}),
        }


class TrainingAnswerForm(forms.Form):
    answer = forms.CharField(label='Ваш перевод', max_length=180, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
