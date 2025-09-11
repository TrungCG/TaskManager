from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.SignupView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    path('tasks/<int:pk>/', views.TaskView.as_view()),
]