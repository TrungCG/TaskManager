from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('auth/register/', views.SignupView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    # path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('tasks/', views.TaskView.as_view()),
    path('tasks/<int:pk>/', views.TaskView.as_view()),
    path('tasks/<int:pk>/uploadFile/', views.TaskFileView.as_view()),
    path('tasks/<int:pk>/deleteFile/', views.TaskFileView.as_view(), name='taskfile-delete'),
    
    path('tags/', views.TagView.as_view()),
    path('tags/<int:pk>/', views.TagView.as_view()),
    
    path('categories/', views.CategoryView.as_view()),
    path('categories/<int:pk>/', views.CategoryView.as_view()),
]