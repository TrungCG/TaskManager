from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignupView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    path('tasks/<int:pk>/', views.TaskView.as_view()),
    path('tasks/<int:pk>/upload/', views.TaskFileView.as_view()),
    path('tags/', views.TagView.as_view()),
    path('tags/<int:pk>/', views.TagView.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('categories/<int:pk>/', views.CategoryView.as_view()),
]