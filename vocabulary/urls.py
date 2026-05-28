from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('words/', views.word_list, name='word_list'),
    path('words/add/', views.word_create, name='word_create'),
    path('words/<int:pk>/', views.word_detail, name='word_detail'),
    path('words/<int:pk>/edit/', views.word_edit, name='word_edit'),
    path('words/<int:pk>/learn/', views.add_to_dictionary, name='add_to_dictionary'),
    path('my-words/', views.my_words, name='my_words'),
    path('my-words/<int:pk>/learned/', views.mark_learned, name='mark_learned'),
    path('my-words/<int:pk>/learning/', views.mark_learning, name='mark_learning'),
    path('my-words/<int:pk>/delete/', views.remove_from_dictionary, name='remove_from_dictionary'),
    path('training/', views.training, name='training'),
    path('quiz/', views.quiz, name='quiz'),
]
