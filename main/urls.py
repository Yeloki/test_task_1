from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostListView.as_view()),
    path('posts/<int:pk>', views.PostView.as_view()),
    path('comments/', views.CommentCreateView.as_view()),
    path('comments/<int:pk>', views.CommentView.as_view()),
    path('users/', views.UserListView.as_view()),
    path('users/<int:pk>', views.UserView.as_view()),
]
