from django.urls import path
from .views import index, RegisterView, profile

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='users-profile'),
]