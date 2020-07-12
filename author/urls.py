from django.urls import path

from author import views

urlpatterns = [
    path('author/<int:id>/', views.AuthorView, name='author'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('follow/<int:id>/', views.FollowView, name='follow'),
    path('unfollow/<int:id>/', views.UnfollowView, name='unfollow'),
]
