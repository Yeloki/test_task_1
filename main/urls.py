from django.urls import path

from . import views

urlpatterns = [
    path('docs', views.docs, name='docs'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('posts/<int:pk>', views.PostView.as_view(), name='post'),
    path('comments/', views.CommentCreateView.as_view(), name='comments'),
    path('comments/<int:pk>', views.CommentView.as_view(), name='comment'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>', views.UserView.as_view(), name='user'),
]
