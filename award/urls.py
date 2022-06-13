from django.urls import path
from .views import index, RegisterView

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
]