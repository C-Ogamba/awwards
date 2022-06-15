from django.urls import path
from . import views
from .views import index, RegisterView, profile, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, update_profile

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='users-profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name='delete_post'),
    path('search/', views.Search, name='search'),
]